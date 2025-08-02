const express = require('express');
const router = express.Router();
const logisticaController = require('../controllers/logisticaController');

router.post('/rota', logisticaController.calcularRotaEntrega);
router.post('/status', logisticaController.atualizarStatusEntrega);

module.exports = router;