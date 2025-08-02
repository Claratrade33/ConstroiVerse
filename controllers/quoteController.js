const Quote = require('../models/Quote');
const Project = require('../models/Project');
const { gerarOrcamentoIA } = require('../utils/iaIntegration');

// 1. Arquiteto gera orçamento via IA
exports.gerarOrcamento = async (req, res) => {
  const { projectId } = req.body;

  const projeto = await Project.findById(projectId);
  const prompt = `Gere um orçamento estimado para os seguintes dados de obra: ${JSON.stringify(projeto)}`;

  const resposta = await gerarOrcamentoIA(prompt);

  // 👇 Exemplo: IA retorna um texto ou JSON com itens
  const novoOrcamento = new Quote({
    project: projectId,
    status: "gerado",
    items: [
      { product: "Tinta branca", quantity: 10 },
      { product: "Massa corrida", quantity: 5 }
    ],
    iaResumo: resposta
  });

  await novoOrcamento.save();
  res.json({ sucesso: true, quote: novoOrcamento });
};