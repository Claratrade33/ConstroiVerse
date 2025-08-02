const Quote = require('../models/Quote');
const Project = require('../models/Project');
const Stock = require('../models/Stock');
const User = require('../models/User');

exports.gerarRelatorioObra = async (req, res) => {
  try {
    const { projectId } = req.params;

    const orcamentos = await Quote.find({ project: projectId });
    const projeto = await Project.findById(projectId);
    const cliente = await User.findById(projeto.architect);

    let custoTotal = 0;
    let recebimentoEstimado = projeto.budget || 0;

    orcamentos.forEach(orc => {
      orc.items.forEach(item => {
        custoTotal += (item.price * item.quantity);
      });
    });

    const roi = recebimentoEstimado > 0 ? ((recebimentoEstimado - custoTotal) / custoTotal) * 100 : 0;

    res.json({
      projeto: projeto.name,
      cliente: cliente.name,
      custoTotal,
      recebimentoEstimado,
      ROI: `${roi.toFixed(2)}%`,
      orcamentos
    });

  } catch (err) {
    res.status(500).json({ erro: err.message });
  }
};