const express = require('express');
const router = express.Router();
const auth = require('../middlewares/auth');
const { register, login } = require('../controllers/userController');

router.post('/register', register);
router.post('/login', login);

router.get('/profile', auth, async (req, res) => {
  // Exemplo de rota protegida
  // Aqui você retornaria informações conforme as configuradas em privacySettings
  res.json({ message: 'Perfil privado visível apenas ao dono ou amigos' });
});

module.exports = router;