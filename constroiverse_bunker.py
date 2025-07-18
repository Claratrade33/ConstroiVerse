import os
from flask import Flask, render_template_string, request, redirect, jsonify
from cryptography.fernet import Fernet
import openai
import sqlite3

# === Segurança ===
FERNET_KEY = b'0dUWR9N3n0N_CAf8jPwjrVzhU3TXw1BkCrnIQ6HvhIA='
CHAVE_CRIPTOGRAFADA = b'gAAAAABoerOcaUWALvY8Vr42IJjyoC1O7iW8NZ284Ic2vOoF4FlYcGu-tuXF7Qi76saV6MftU5McTiMMiAd6Hb8JxcrhWWi-HLRxx0o4aEH74X7-4b3hltdavirtw64hsyOSGm6MemlP'
fernet = Fernet(FERNET_KEY)
openai.api_key = fernet.decrypt(CHAVE_CRIPTOGRAFADA).decode()

# === Flask App ===
app = Flask(__name__)

# === Banco de dados simples ===
def init_db():
    conn = sqlite3.connect("constroiverse.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orcamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        itens TEXT,
        valor_total TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# === Página inicial ===
HTML_INDEX = """
<!DOCTYPE html>
<html>
<head>
    <title>ConstroiVerse</title>
    <style>
        body {
            background-color: #0d0d0d;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 60px;
        }
        button {
            background-color: #00ffcc;
            color: black;
            padding: 20px 40px;
            font-size: 22px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 0 15px #00ffcc;
        }
        button:hover {
            background-color: #00ccaa;
        }
    </style>
</head>
<body>
    <h1>🧱 Bem-vindo ao ConstroiVerse</h1>
    <p>IA Clarice pronta para iniciar sua jornada de construção inteligente.</p>
    <form action="/painel">
        <button>INICIAR CONSTRUÇÃO DA MINHA OBRA</button>
    </form>
</body>
</html>
"""

# === Painel com IA Clarice ===
HTML_PAINEL = """
<!DOCTYPE html>
<html>
<head>
    <title>Painel da Obra - ConstroiVerse</title>
    <style>
        body {
            background-color: #111;
            color: white;
            font-family: Arial;
            padding: 40px;
        }
        textarea {
            width: 100%;
            height: 100px;
            padding: 10px;
        }
        button {
            margin-top: 10px;
            padding: 15px;
            background: #00ffcc;
            border: none;
            font-size: 18px;
            border-radius: 8px;
            cursor: pointer;
        }
        .resposta {
            background: #1a1a1a;
            padding: 20px;
            margin-top: 20px;
            border-left: 5px solid #00ffcc;
        }
    </style>
</head>
<body>
    <h2>IA Clarice — Consultora da sua Obra</h2>
    <form method="POST">
        <textarea name="pergunta" placeholder="Ex: Qual o melhor piso para área externa?"></textarea><br>
        <button type="submit">Perguntar à Clarice</button>
    </form>
    {% if resposta %}
    <div class="resposta">
        <strong>Resposta da Clarice:</strong><br>
        {{ resposta }}
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_INDEX)

@app.route("/painel", methods=["GET", "POST"])
def painel():
    resposta = ""
    if request.method == "POST":
        pergunta = request.form["pergunta"]
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Você é Clarice, uma consultora especializada em obras e construção civil."},
                    {"role": "user", "content": pergunta}
                ]
            )
            resposta = completion.choices[0].message.content
        except Exception as e:
            resposta = f"Erro ao consultar a IA Clarice: {e}"
    return render_template_string(HTML_PAINEL, resposta=resposta)

# === Aplicação para Render ===
if __name__ == "__main__":
    app.run(debug=True)
else:
    application = app

