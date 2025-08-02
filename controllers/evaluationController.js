const Evaluation = require('../models/Evaluation');
const User = require('../models/User');

// Avaliação com nota e comentário
exports.avaliarUsuario = async (req, res) => {
  try {
    const { avaliadoId, nota, comentario, tipo } = req.body;
    const autorId = req.user.id;

    const nova = new Evaluation({
      avaliado: avaliadoId,
      autor: autorId,
      nota,
      comentario,
      tipo
    });

    await nova.save();

    // Atualiza média de avaliação no User (futuro cálculo real)
    const avaliacoes = await Evaluation.find({ avaliado: avaliadoId });
    const media = (avaliacoes.reduce((a, b) => a + b.nota, 0) / avaliacoes.length).toFixed(2);

    await User.findByIdAndUpdate(avaliadoId, { reputacao: media });

    res.json({ sucesso: true, mensagem: "Avaliação registrada com sucesso", mediaAtualizada: media });
  } catch (err) {
    res.status(500).json({ sucesso: false, erro: err.message });
  }
};