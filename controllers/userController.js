const User = require('../models/User');

exports.listarUsuarios = async (req, res) => {
  try {
    const usuarios = await User.find();
    res.json(usuarios);
  } catch (err) {
    res.status(500).json({ error: 'Erro ao buscar usuários' });
  }
};

exports.criarUsuario = async (req, res) => {
  try {
    const usuario = new User(req.body);
    await usuario.save();
    res.status(201).json(usuario);
  } catch (err) {
    res.status(400).json({ error: 'Erro ao criar usuário' });
  }
};

