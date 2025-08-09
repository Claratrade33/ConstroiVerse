const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

router.get('/', userController.listarUsuarios);
router.post('/', userController.criarUsuario);

module.exports = router;
