require('dotenv').config();
const express = require('express');
const cors = require('cors');
const app = express();

const userRoutes = require('./src/routes/userRoutes');
const projectRoutes = require('./src/routes/projectRoutes');

app.use(cors());
app.use(express.json());

// Rotas principais
app.use('/api/users', userRoutes);
app.use('/api/projects', projectRoutes);

app.get('/', (req, res) => {
  res.send('API ConstroiVerse ativa!');
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => console.log(`Servidor rodando na porta ${PORT}`));