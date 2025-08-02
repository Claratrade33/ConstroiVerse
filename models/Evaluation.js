const mongoose = require('mongoose');

const EvaluationSchema = new mongoose.Schema({
  avaliado: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  autor: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  nota: { type: Number, min: 1, max: 5, required: true },
  comentario: { type: String, default: "" },
  tipo: { type: String, enum: ['servico', 'entrega', 'produto'], default: 'servico' },
  data: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Evaluation', EvaluationSchema);