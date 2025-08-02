const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  name: String,
  email: { type: String, unique: true },
  password: String,

  // Perfil principal (ex: loja, construtora, pintor, cliente, arquiteto, etc.)
  mainProfile: {
    type: String,
    enum: [
      'loja',
      'fabricante',
      'construtora',
      'arquiteto',
      'engenheiro',
      'pintor',
      'pedreiro',
      'corretor',
      'cliente',
      'mestre_obra',
      'representante',
      'instalador'
    ],
    required: true
  },

  // Subperfil (ex: gerente, vendedor, financeiro...)
  role: {
    type: String,
    enum: ['gerente', 'vendedor', 'estoquista', 'financeiro', 'atendente', 'profissional', 'admin', 'cliente'],
    default: 'cliente'
  },

  permissions: {
    type: [String], // Ex: ['ver_estoque', 'criar_orcamento', 'editar_preco']
    default: []
  },

  active: { type: Boolean, default: true },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('User', UserSchema);