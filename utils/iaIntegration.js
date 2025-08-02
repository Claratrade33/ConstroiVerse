const { Configuration, OpenAIApi } = require("openai");

// A chave de API será lida do .env ou do banco se configurado
const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
});
const openai = new OpenAIApi(configuration);

// Função principal: Geração de orçamento com base em texto
async function gerarOrcamentoIA(texto) {
  const response = await openai.createChatCompletion({
    model: "gpt-4",
    messages: [
      {
        role: "system",
        content: "Você é uma IA especialista em construção civil, orçamento de materiais e análise de superfícies para pintura, reforma e acabamento.",
      },
      {
        role: "user",
        content: texto
      }
    ],
    temperature: 0.4
  });

  return response.data.choices[0].message.content;
}

// Simulação: Cálculo de materiais para pintura (baseado em área estimada)
async function calcularMaterialPintura(areaM2) {
  const litrosPorM2 = 0.1; // 1L para cada 10m²
  return {
    tintaLitros: (areaM2 * litrosPorM2).toFixed(2),
    massaCorridaKg: (areaM2 * 0.45).toFixed(1),
    rolos: Math.ceil(areaM2 / 30),
    pincéis: Math.ceil(areaM2 / 50),
    lixas: Math.ceil(areaM2 / 25),
  };
}

// Simulação: Análise de imagem (área estimada) — futura integração com IA Vision
async function estimarAreaPorImagem(filePath) {
  // Integração futura com IA Vision (OpenAI, Clarifai, etc.)
  return 40; // Ex: retorna 40m² estimado
}

module.exports = {
  gerarOrcamentoIA,
  calcularMaterialPintura,
  estimarAreaPorImagem
};