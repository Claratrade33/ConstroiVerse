import os
from flask import Flask, render_template_string, request, jsonify
from cryptography.fernet import Fernet
import openai

# Chave criptografada (exemplo)
FERNET_KEY = "0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA="
fernet = Fernet(FERNET_KEY)

# Chave da OpenAI protegida
encrypted_openai_key = "gAAAAABmZNuu...SUFIXO_SEGURO"
openai.api_key = fernet.decrypt(encrypted_openai_key.encode()).decode()

# App Flask
app = Flask(__name__)

# Página principal com interface Clarice
TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Clarice | Orçamentos Inteligentes</title>
    <style>
        body {
            background: #10131A;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            margin: 0;
            padding: 0;
        }
        header {
            background: #1C1F2A;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            color: #00FFC6;
        }
        section {
            padding: 40px;
        }
        .bloco {
            background: #1A1D27;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 0 8px #00FFC633;
        }
        h2 {
            color: #00FFC6;
            font-size: 20px;
            margin-top: 0;
        }
        ul {
            padding-left: 20px;
        }
        li {
            margin-bottom: 8px;
        }
        textarea {
            width: 100%;
            height: 120px;
            background: #0F1117;
            border: none;
            color: #00FFC6;
            font-size: 16px;
            padding: 10px;
            margin-top: 10px;
        }
        button {
            padding: 10px 20px;
            background: #00FFC6;
            border: none;
            color: #000;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <header>🧠 Clarice | Orçamentos Inteligentes</header>
    <section>
        <div class="bloco">
            <h2>✅ Funções Atuais</h2>
            <ul>
                <li>🛠️ Cadastro de obras, materiais e fornecedores</li>
                <li>🧮 Calculadora de obra e financiamento</li>
                <li>🏠 Interface de gerenciamento para construtora</li>
                <li>🧠 IA Clarice entre arquiteto, loja e cliente</li>
                <li>🛍️ Lojas respondem orçamentos direto</li>
                <li>💰 Respostas automáticas de vendedores</li>
                <li>📊 Relatórios, previsões e histórico</li>
                <li>👨‍👩‍👧 Impacto humano: tempo, paz, harmonia</li>
            </ul>
        </div>
        <div class="bloco">
            <h2>🚧 Em Desenvolvimento</h2>
            <ul>
                <li>🤖 Conversas com clientes, fornecedores e arquitetos</li>
                <li>⛏️ Lembrar pedreiro sobre entregas</li>
                <li>🧾 Criar orçamentos automáticos e otimizados</li>
                <li>🔁 Propor mudanças de custo/qualidade</li>
                <li>📡 Visão em tempo real para todos envolvidos</li>
            </ul>
        </div>
        <div class="bloco">
            <h2>💬 Fale com a Clarice</h2>
            <form method="post" action="/">
                <textarea name="pergunta" placeholder="Digite sua pergunta..."></textarea>
                <button type="submit">Perguntar</button>
            </form>
            {% if resposta %}
                <div class="bloco">
                    <h2>🧠 Resposta da Clarice:</h2>
                    <p>{{ resposta }}</p>
                </div>
            {% endif %}
        </div>
    </section>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    resposta = None
    if request.method == "POST":
        pergunta = request.form.get("pergunta")
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": pergunta}]
            )
            resposta = completion.choices[0].message.content
        except Exception as e:
            resposta = f"Erro ao consultar Clarice: {e}"
    return render_template_string(TEMPLATE_HTML, resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)
