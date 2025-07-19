from flask import Flask, request, render_template_string
import os
import openai

# Configurar a chave da OpenAI usando variável de ambiente
openai.api_key = os.getenv("OPENAI")

app = Flask(__name__)

# HTML da página inicial
index_html = """
<!DOCTYPE html>
<html lang='pt-br'>
<head>
  <meta charset='UTF-8'>
  <title>ConstroiVerse</title>
  <style>
    body {{
      background-color: #0a0a0a;
      color: white;
      font-family: 'Arial', sans-serif;
      text-align: center;
      padding-top: 80px;
    }}
    a {{
      display: inline-block;
      margin-top: 40px;
      padding: 16px 28px;
      background-color: #00ffc3;
      color: black;
      text-decoration: none;
      font-weight: bold;
      border-radius: 10px;
      box-shadow: 0 0 12px #00ffc366;
    }}
  </style>
</head>
<body>
  <h1>💎 Bem-vindo ao ConstroiVerse</h1>
  <p>Sua obra começa aqui com inteligência.</p>
  <a href='/clarice'>INICIAR CONSTRUÇÃO DA MINHA OBRA</a>
</body>
</html>
"""

# HTML da página da IA Clarice
clarice_html = """
<!DOCTYPE html>
<html lang='pt-br'>
<head>
  <meta charset='UTF-8'>
  <title>Clarice - Assistente de Obra</title>
  <style>
    body {{
      background-color: #111;
      color: white;
      font-family: Arial, sans-serif;
      padding: 30px;
    }}
    textarea {{
      width: 100%;
      height: 120px;
      padding: 10px;
      font-size: 16px;
    }}
    button {{
      padding: 12px 20px;
      background-color: #00ffc3;
      border: none;
      font-weight: bold;
      font-size: 16px;
      border-radius: 6px;
      margin-top: 10px;
      cursor: pointer;
    }}
    .resposta {{
      margin-top: 30px;
      background: #1c1c1c;
      padding: 20px;
      border-left: 4px solid #00ffc3;
      border-radius: 8px;
    }}
  </style>
</head>
<body>
  <h2>👷‍♀️ IA Clarice — Assistente de Obra</h2>
  <form method='POST'>
    <label>Digite sua dúvida ou lista de materiais:</label><br>
    <textarea name='pergunta' placeholder='Ex: Qual a diferença entre telha cerâmica e metálica?'></textarea><br>
    <button type='submit'>Perguntar à Clarice</button>
  </form>
  {% if resposta %}
    <div class='resposta'>
      <strong>Clarice diz:</strong><br>{{ resposta }}
    </div>
  {% endif %}
</body>
</html>
"""

# Função de resposta da IA Clarice
def perguntar_clarice(pergunta):
    try:
        resposta = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é Clarice, uma assistente de obra inteligente, organizada, empática. Ajude clientes, pedreiros, arquitetos e lojistas com dúvidas sobre construção, obra, materiais, orçamento e reforma."},
                {"role": "user", "content": pergunta}
            ]
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro com Clarice: {str(e)}"

# Rotas
@app.route("/")
def index():
    return render_template_string(index_html)

@app.route("/clarice", methods=["GET", "POST"])
def clarice():
    resposta = ""
    if request.method == "POST":
        pergunta = request.form.get("pergunta", "")
        resposta = perguntar_clarice(pergunta)
    return render_template_string(clarice_html, resposta=resposta)

# Para rodar no Render
if __name__ == "__main__":
    app.run(debug=True)
else:
    application = app