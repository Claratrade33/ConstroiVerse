const mongoose = require('mongoose');

const DeliverySchema = new mongoose.Schema({
  quote: { type: mongoose.Schema.Types.ObjectId, ref: 'Quote' },
  supplier: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  client: { type: mongoose.Schema.Types.ObjectId, ref: 'User' },
  address: String,
  scheduledAt: Date,
  status: { type: String, enum: ['pendente', 'em rota', 'entregue', 'atrasado'], default: 'pendente' },
  estimatedArrival: Date,
  realArrival: Date,
  priority: Number, // 1 = alta, 3 = baixa
  gpsRoute: [String] // coordenadas da rota
});

module.exports = mongoose.model('Delivery', DeliverySchema);