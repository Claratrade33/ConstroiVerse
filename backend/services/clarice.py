import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# 🔮 Função principal da IA Clarice
def gerar_orcamento(texto_descricao):
    prompt = f"""
Você é uma engenheira de obras chamada Clarice. 
A partir da descrição abaixo, gere um orçamento estimado com:

- Lista de materiais básicos
- Quantidades aproximadas
- Preço médio estimado por item
- Cronograma em etapas (dias)
- Observações técnicas ou sugestões

Descrição do projeto:
{texto_descricao}

Responda em JSON estruturado com as chaves: materiais, cronograma, total_estimado, observacoes.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=800
        )

        texto_resposta = response.choices[0].message.content
        return texto_resposta

    except Exception as e:
        return {"erro": str(e)}