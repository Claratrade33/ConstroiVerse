from flask import Flask, request, render_template_string
import openai

# 🔐 Chave da OpenAI já embutida no bunker
openai.api_key = "sk-..."

app = Flask(__name__)

# 🧠 Template HTML com IA Clarice implantada
clarice_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ConstróiVerse | Clarice IA</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background: #0d0d0d;
            color: #e0f7fa;
            font-family: 'Segoe UI', sans-serif;
            padding: 30px;
        }
        .container {
            max-width: 900px;
            margin: auto;
        }
        h1, h2 {
            color: #00e6e6;
            text-align: center;
        }
        textarea {
            width: 100%;
            height: 120px;
            background: #1a1a1a;
            border: 1px solid #00cccc;
            color: #fff;
            padding: 10px;
            border-radius: 8px;
            font-size: 16px;
            resize: none;
        }
        button {
            margin-top: 15px;
            padding: 12px 24px;
            background-color: #00e6e6;
            border: none;
            border-radius: 8px;
            color: #000;
            font-weight: bold;
            cursor: pointer;
        }
        .bloco {
            margin-top: 40px;
            background: #111;
            border-left: 6px solid #00cccc;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px #00cccc66;
        }
        ul {
            list-style-type: "🛠️ ";
            padding-left: 20px;
        }
        ul li {
            margin-bottom: 8px;
        }
        .resposta {
            margin-top: 30px;
            padding: 20px;
            background: #222;
            border-left: 6px solid #00e6e6;
            border-radius: 8px;
        }
        a {
            color: #00cccc;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Clarice - Assistente de Construção</h1>
        <p style="text-align: center;">Digite seu orçamento, projeto ou dúvida:</p>
        
        <form method="POST">
            <textarea name="pergunta" placeholder="Ex: Preciso construir uma casa de 3 quartos com acabamento médio..."></textarea>
            <button type="submit">Analisar</button>
        </form>

        {% if resposta %}
            <div class="resposta">
                <strong>Resposta da Clarice:</strong><br>
                {{ resposta }}
            </div>
        {% endif %}

        <div class="bloco">
            <h2>📋 Tela de Orçamentos Inteligentes</h2>
            <ul>
                <li>Módulo de cadastro de obras, materiais, fornecedores</li>
                <li>Calculadora de obra e financiamento automático</li>
                <li>Interface da construtora com gerenciamento total</li>
                <li>IA Clarice organizando tudo entre arquiteto, loja e cliente</li>
                <li>Lojas podendo responder orçamentos direto na plataforma</li>
                <li>Impacto humano visível (tempo com família, paz, menos briga)</li>
                <li>Vendedores respondendo orçamentos com 1 clique</li>
                <li>Relatórios, alertas, previsões e histórico completo</li>
            </ul>
        </div>

        <div class="bloco">
            <h2>🚀 Clarice ainda vai fazer:</h2>
            <ul style="list-style-type: '🧠 '; padding-left: 20px;">
                <li>Conversar com fornecedores, clientes e arquitetos</li>
                <li>Lembrar o pedreiro do que precisa chegar</li>
                <li>Informar o arquiteto do valor e prazos reais</li>
                <li>Criar orçamentos inteligentes</li>
                <li>Propor mudanças para reduzir custo ou aumentar qualidade</li>
                <li>Mostrar tudo em tempo real pro cliente e pro dono da obra</li>
            </ul>
        </div>

        <p style="text-align:center; margin-top: 40px;"><a href="/">← Voltar ao início</a></p>
    </div>
</body>
</html>
"""

# 🌐 Rota principal Clarice
@app.route("/", methods=["GET", "POST"])
def clarice():
    resposta = None
    if request.method == "POST":
        pergunta = request.form.get("pergunta", "")
        if pergunta.strip():
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Você é a IA Clarice, especialista em obras e construções. Dê respostas objetivas, humanas e úteis."},
                        {"role": "user", "content": pergunta}
                    ],
                    temperature=0.7,
                    max_tokens=600
                )
                resposta = completion.choices[0].message.content.strip()
            except Exception as e:
                resposta = f"Erro ao consultar a IA: {str(e)}"
    return render_template_string(clarice_html, resposta=resposta)

# ✅ Rodando o app
if __name__ == "__main__":
    app.run(debug=True)