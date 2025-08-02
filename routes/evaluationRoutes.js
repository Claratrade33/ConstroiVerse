const express = require('express');
const router = express.Router();
const evaluationController = require('../controllers/evaluationController');
const auth = require('../middlewares/auth');

router.post('/avaliar', auth, evaluationController.avaliarUsuario);

module.exports = router;