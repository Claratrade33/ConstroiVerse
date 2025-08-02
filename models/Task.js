const mongoose = require('mongoose');

const TaskSchema = new mongoose.Schema({
  project: { type: mongoose.Schema.Types.ObjectId, ref: 'Project' },
  title: String,
  description: String,
  assignedTo: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  createdBy: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  status: { type: String, enum: ['pendente', 'em andamento', 'concluída'], default: 'pendente' },
  dueDate: Date,
  completedAt: Date
});

module.exports = mongoose.model('Task', TaskSchema);