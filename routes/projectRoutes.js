const express = require('express');
const router = express.Router();
const projectController = require('../controllers/projectController');

router.get('/', projectController.listarProjetos);
router.post('/', projectController.criarProjeto);

module.exports = router;
