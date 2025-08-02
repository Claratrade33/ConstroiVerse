const express = require('express');
const router = express.Router();
const deliveryController = require('../controllers/deliveryController');

router.post('/', deliveryController.criarEntrega);
router.get('/:supplierId', deliveryController.listaEntregas);
router.put('/:entregaId/status', deliveryController.atualizarStatus);

module.exports = router;