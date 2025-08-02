const Delivery = require('../models/Delivery');
const Quote = require('../models/Quote');

// Cadastra nova entrega
exports.criarEntrega = async (req, res) => {
  const nova = new Delivery(req.body);
  await nova.save();
  res.json(nova);
};

// Lista entregas por fornecedor (em ordem de prioridade e horário)
exports.listaEntregas = async (req, res) => {
  const entregas = await Delivery.find({ supplier: req.params.supplierId })
    .sort({ priority: 1, scheduledAt: 1 });
  res.json(entregas);
};

// Atualiza status de entrega (em rota, entregue, atrasado)
exports.atualizarStatus = async (req, res) => {
  const { entregaId } = req.params;
  const { status } = req.body;
  const entrega = await Delivery.findById(entregaId);
  entrega.status = status;
  if (status === 'entregue') entrega.realArrival = new Date();
  await entrega.save();
  res.json(entrega);
};