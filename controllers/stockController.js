const Stock = require('../models/Stock');
const Quote = require('../models/Quote');

// 2. Loja/Fábrica responde a orçamento
exports.responderOrcamento = async (req, res) => {
  const { quoteId, fornecedorId } = req.body;

  const quote = await Quote.findById(quoteId);
  const estoque = await Stock.findOne({ owner: fornecedorId });

  const resposta = quote.items.map(item => {
    const produto = estoque.products.find(p => p.product === item.product);
    if (produto && produto.quantity >= item.quantity) {
      return { ...item, disponibilidade: "imediata", fornecedor: fornecedorId };
    } else {
      return { ...item, disponibilidade: "sob demanda", fornecedor: fornecedorId };
    }
  });

  quote.status = "respondido";
  quote.items = resposta;
  await quote.save();

  res.json({ sucesso: true, resposta });
};