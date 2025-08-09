const Project = require('../models/Project');

exports.listarProjetos = async (req, res) => {
  try {
    const projetos = await Project.find();
    res.json(projetos);
  } catch (err) {
    res.status(500).json({ error: 'Erro ao buscar projetos' });
  }
};

exports.criarProjeto = async (req, res) => {
  try {
    const projeto = new Project(req.body);
    await projeto.save();
    res.status(201).json(projeto);
  } catch (err) {
    res.status(400).json({ error: 'Erro ao criar projeto' });
  }
};

