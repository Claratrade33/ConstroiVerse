from flask import Flask, request, render_template_string
import os
import openai

# Configurar chave da OpenAI via variável de ambiente
openai.api_key = os.getenv("OPENAI")

app = Flask(__name__)

# HTML da página inicial
index_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>ConstroiVerse</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap">
    <style>
        body {
            background-color: #0a0a0a;
            color: white;
            font-family: 'Orbitron', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        a.botao {
            background-color: #00ffc3;
            color: black;
            padding: 14px 24px;
            text-decoration: none;
            font-weight: bold;
            border-radius: 8px;
            box-shadow: 0 0 10px #00ffc366;
        }
    </style>
</head>
<body>
    <h2>🔩 Bem-vindo ao ConstroiVerse</h2>
    <p>A IA Clarice está pronta para te ajudar.</p>
    <a href="/clarice" class="botao">INICIAR CONSTRUÇÃO DA MINHA OBRA</a>
</body>
</html>
"""

# HTML da página da IA Clarice
clarice_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Clarice - Assistente de Obra</title>
    <style>
        body {
            background-color: #0f0f0f;
            color: #fff;
            font-family: 'Arial', sans-serif;
            padding: 20px;
        }
        textarea, input[type=submit] {
            width: 100%;
            padding: 10px;
            margin-top: 10px;
            font-size: 16px;
        }
        input[type=submit] {
            background-color: #00ffc3;
            color: black;
            font-weight: bold;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        .resposta {
            margin-top: 20px;
            padding: 15px;
            background: #1a1a1a;
            border-left: 4px solid #00ffc3;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <h2>👷‍♀️ IA Clarice 🏗️ Assistente de Obra</h2>
    <form method="post">
        <label>Digite sua dúvida ou lista de materiais:</label>
        <textarea name="pergunta" rows="4" placeholder="Ex: Qual a diferença entre piso porcelanato e vinílico?"></textarea>
        <input type="submit" value="Perguntar à Clarice">
    </form>

    {% if resposta %}
    <div class="resposta">
        <strong>Clarice diz:</strong><br>
        {{ resposta }}
    </div>
    {% endif %}
</body>
</html>
"""

def perguntar_clarice(pergunta):
    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é Clarice, uma assistente de obra inteligente, calma e bem organizada. Sua missão é ajudar pessoas em construções, obras, reformas, materiais, e planejamento, de forma prática e empática."
                },
                {"role": "user", "content": pergunta}
            ]
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro com Clarice: {str(e)}"

@app.route("/")
def index():
    return render_template_string(index_html)

@app.route("/clarice", methods=["GET", "POST"])
def clarice():
    resposta = ""
    if request.method == "POST":
        pergunta = request.form.get("pergunta")
        resposta = perguntar_clarice(pergunta)
    return render_template_string(clarice_html, resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)
