const express = require('express');
const router = express.Router();
const reportController = require('../controllers/reportController');

router.get('/obra/:projectId', reportController.gerarRelatorioObra);

module.exports = router;