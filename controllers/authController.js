const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models/User');

exports.register = async (req, res) => {
  try {
    const { name, email, password, mainProfile } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);

    const user = await User.create({
      name,
      email,
      password: hashedPassword,
      mainProfile,
      role: 'user',
      permissions: []
    });

    const token = jwt.sign(
      { id: user._id, mainProfile: user.mainProfile, role: user.role, permissions: user.permissions },
      process.env.JWT_SECRET,
      { expiresIn: '12h' }
    );

    res.status(201).json({
      sucesso: true,
      token,
      redirect: `/painel/${user.mainProfile}`,
      perfil: user.mainProfile,
      role: user.role,
      permissions: user.permissions
    });
  } catch (err) {
    res.status(500).json({ sucesso: false, erro: err.message });
  }
};

exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ sucesso: false, erro: 'Usuário não encontrado' });

    const senhaCorreta = await bcrypt.compare(password, user.password);
    if (!senhaCorreta) return res.status(401).json({ sucesso: false, erro: 'Senha incorreta' });

    const token = jwt.sign(
      { id: user._id, mainProfile: user.mainProfile, role: user.role, permissions: user.permissions },
      process.env.JWT_SECRET,
      { expiresIn: '12h' }
    );

    res.json({
      sucesso: true,
      token,
      redirect: `/painel/${user.mainProfile}`, // 🔁 redirecionamento por perfil
      perfil: user.mainProfile,
      role: user.role,
      permissions: user.permissions
    });
  } catch (err) {
    res.status(500).json({ sucesso: false, erro: err.message });
  }
};

module.exports = {
  register: exports.register,
  login: exports.login
};

