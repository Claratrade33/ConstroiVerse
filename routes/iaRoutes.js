const express = require('express');
const router = express.Router();
const Clarice = require('../utils/clariceIA');

router.get('/executar', async (req, res) => {
  await Clarice.executarIA();
  res.json({ status: 'IA Clarice executou redistribuições.' });
});

module.exports = router;