const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const app = express();
const PORT = 3000;

// Configurações
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, '../frontend')));
app.set('views', path.join(__dirname, '../frontend'));
app.set('view engine', 'ejs');

// Rota inicial: seleção de perfil
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/index.html'));
});

// Rota de login por perfil (ex: /login?perfil=arquiteto)
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, '../frontend/login.html'));
});

// Rota POST de painel após login (será ajustada para cada perfil)
app.post('/painel', (req, res) => {
  const { email, senha, perfil } = req.body;

  // Aqui entra a lógica de autenticação (mock por enquanto)
  console.log(`Usuário: ${email}, Perfil: ${perfil}`);

  // Redireciona para painel do perfil (ex: /painel/arquiteto)
  res.redirect(`/painel/${perfil}`);
});

// Rota de painel por perfil
app.get('/painel/:perfil', (req, res) => {
  const perfil = req.params.perfil;
  res.send(`<h1>Painel do ${perfil.charAt(0).toUpperCase() + perfil.slice(1)}</h1><p>Bem-vindo(a) ao ConstroiVerse!</p>`);
});

// Inicia o servidor
app.listen(PORT, () => {
  console.log(`🌐 Servidor rodando em http://localhost:${PORT}`);
});