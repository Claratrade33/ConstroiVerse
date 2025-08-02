const Task = require('../models/Task');

exports.criarTarefa = async (req, res) => {
  const novaTarefa = new Task(req.body);
  await novaTarefa.save();
  res.json(novaTarefa);
};

exports.listarTarefasPorProjeto = async (req, res) => {
  const tarefas = await Task.find({ project: req.params.projectId }).populate('assignedTo', 'name').populate('createdBy', 'name');
  res.json(tarefas);
};

exports.atualizarStatus = async (req, res) => {
  const { taskId } = req.params;
  const { status } = req.body;
  const tarefa = await Task.findById(taskId);
  tarefa.status = status;
  if (status === 'concluída') tarefa.completedAt = new Date();
  await tarefa.save();
  res.json(tarefa);
};