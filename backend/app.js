const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

// Middlewares
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../frontend')));

// Rotas fixas
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Rota de login por perfil (ex: /login?perfil=arquiteto)
app.get('/login', (req, res) => {
  const perfil = req.query.perfil;
  if (!perfil) {
    return res.sendFile(path.join(__dirname, '../frontend/login/login.html'));
  }
  res.sendFile(path.join(__dirname, `../frontend/login/login_${perfil}.html`));
});

// Painéis por perfil (ex: /painel/engenheiro → painel_engenheiro.html)
app.get('/painel/:perfil', (req, res) => {
  const perfil = req.params.perfil;
  res.sendFile(path.join(__dirname, `../frontend/painel/painel_${perfil}.html`));
});

// Start do servidor
app.listen(PORT, () => {
  console.log(`✅ Servidor rodando: http://localhost:${PORT}`);
});