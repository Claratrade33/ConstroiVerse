const Task = require('../models/Task');
const Delivery = require('../models/Delivery');
const User = require('../models/User');

// Redistribuição de tarefas atrasadas
exports.redistribuirTarefas = async () => {
  const tarefasAtrasadas = await Task.find({ status: 'atrasado' });
  for (let tarefa of tarefasAtrasadas) {
    const outros = await User.find({ profile: 'pedreiro', _id: { $ne: tarefa.assignedTo } });
    if (outros.length > 0) {
      tarefa.assignedTo = outros[Math.floor(Math.random() * outros.length)]._id;
      tarefa.status = 'redistribuido';
      await tarefa.save();
    }
  }
};

// Entregas atrasadas → nova previsão
exports.ajustarEntregas = async () => {
  const atrasadas = await Delivery.find({ status: 'em rota', estimatedArrival: { $lt: new Date() } });
  for (let entrega of atrasadas) {
    entrega.status = 'atrasado';
    entrega.estimatedArrival = new Date(Date.now() + 60 * 60 * 1000); // adia 1h
    await entrega.save();
  }
};

// Função geral da IA
exports.executarIA = async () => {
  await exports.redistribuirTarefas();
  await exports.ajustarEntregas();
  console.log('Clarice IA executou redistribuição e previsão.');
};