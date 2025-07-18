
import os
from flask import Flask, render_template_string, request
from cryptography.fernet import Fernet
import openai
import sqlite3

FERNET_KEY = b"zcEp99AQzcHhVddY6fuInXuk9ZLtHQ0lLBcwjs2s_-Q="
CHAVE_CRIPTOGRAFADA = b"gAAAAABoescWePjrpCUPgEHl99XFf2or46RyYvgkAA4uE_7M6H8-BkLHdNUD8Z8qfrZTcFimPOlIDINeZFWWlgqnuFXDgMRDgecLmyvtohmQDBHjAuoUgkk2h5irzXfbRYtX40F7CwqX"
fernet = Fernet(FERNET_KEY)
openai.api_key = fernet.decrypt(CHAVE_CRIPTOGRAFADA).decode()

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("constroiverse.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orcamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            perfil TEXT,
            nome TEXT,
            itens TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()
init_db()

HTML_INDEX = """
<!DOCTYPE html>
<html><head><title>ConstroiVerse</title><style>
body { background:#0d0d0d; color:#fff; text-align:center; padding:50px; font-family:sans-serif }
button { background:#00ffcc; border:none; padding:20px; border-radius:10px; font-size:20px; cursor:pointer }
</style></head><body>
<h1>ð Bem-vindo ao ConstroiVerse</h1>
<p>A IA Clarice estÃ¡ pronta para te ajudar.</p>
<form action='/painel'><button>INICIAR CONSTRUÃÃO DA MINHA OBRA</button></form>
</body></html>
"""

HTML_PAINEL = """
<!DOCTYPE html>
<html><head><title>Painel - Clarice</title><style>
body { background:#111; color:white; font-family:sans-serif; padding:30px }
textarea { width:100%; height:120px; padding:10px; font-size:16px }
button { margin-top:10px; padding:12px; background:#00ffcc; border:none; font-size:16px; border-radius:6px; cursor:pointer }
.resposta { margin-top:20px; background:#222; padding:20px; border-left:5px solid #00ffcc }
</style></head><body>
<h2>ð·ââï¸ IA Clarice â Assistente de Obra</h2>
<form method="post">
<label>Digite sua dÃºvida ou lista de materiais:</label><br>
<textarea name="pergunta" placeholder="Ex: Qual a diferenÃ§a entre piso porcelanato e vinÃ­lico?"></textarea><br>
<button type="submit">Perguntar Ã  Clarice</button>
</form>
{% if resposta %}
<div class="resposta"><strong>Clarice diz:</strong><br>{{ resposta }}</div>
{% endif %}
</body></html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_INDEX)

@app.route("/painel", methods=["GET", "POST"])
def painel():
    resposta = ""
    if request.method == "POST":
        pergunta = request.form.get("pergunta", "")
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "VocÃª Ã© Clarice, uma assistente de inteligÃªncia da construÃ§Ã£o civil. Responda com empatia, clareza e dados tÃ©cnicos sempre que possÃ­vel."},
                    {"role": "user", "content": pergunta}
                ]
            )
            resposta = completion.choices[0].message.content
        except Exception as e:
            resposta = f"Erro com Clarice: {e}"
    return render_template_string(HTML_PAINEL, resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True)
else:
    application = app
