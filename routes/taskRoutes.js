const express = require('express');
const router = express.Router();
const taskController = require('../controllers/taskController');

router.post('/', taskController.criarTarefa);
router.get('/:projectId', taskController.listarTarefasPorProjeto);
router.put('/status/:taskId', taskController.atualizarStatus);

module.exports = router;