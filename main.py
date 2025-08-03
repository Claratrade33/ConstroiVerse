from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import jwt
import datetime
import openai
import os

# Carregar variáveis do .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurações
SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Conexão MongoDB
client = MongoClient(MONGO_URI)
db = client.constroiverse

# Autenticação JWT
def criar_token(usuario):
    payload = {
        "usuario": usuario,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["usuario"]
    except:
        return None

# Middleware de autenticação
def protegido(f):
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            return jsonify({"erro": "Sem token"}), 401
        usuario = verificar_token(auth)
        if not usuario:
            return jsonify({"erro": "Token inválido"}), 403
        return f(usuario, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ===== ROTAS PRINCIPAIS =====

@app.route("/api/login", methods=["POST"])
def login():
    dados = request.json
    usuario = dados.get("usuario")
    senha = dados.get("senha")

    user = db.usuarios.find_one({"usuario": usuario, "senha": senha})
    if not user:
        return jsonify({"erro": "Credenciais inválidas"}), 401

    token = criar_token(usuario)
    return jsonify({"token": token})

@app.route("/api/obras", methods=["GET"])
@protegido
def listar_obras(usuario):
    obras = list(db.obras.find({"usuario": usuario}))
    for o in obras:
        o["_id"] = str(o["_id"])
    return jsonify(obras)

@app.route("/api/tarefas", methods=["POST"])
@protegido
def criar_tarefa(usuario):
    dados = request.json
    dados["usuario"] = usuario
    dados["status"] = "pendente"
    db.tarefas.insert_one(dados)
    return jsonify({"mensagem": "Tarefa criada"})

@app.route("/api/tarefas/<id>/status", methods=["PATCH"])
@protegido
def atualizar_tarefa(usuario, id):
    novo_status = request.json.get("status")
    db.tarefas.update_one({"_id": id, "usuario": usuario}, {"$set": {"status": novo_status}})
    return jsonify({"mensagem": "Status atualizado"})

@app.route("/api/orcamentos", methods=["POST"])
@protegido
def enviar_orcamento(usuario):
    dados = request.json
    dados["usuario"] = usuario
    db.orcamentos.insert_one(dados)
    return jsonify({"mensagem": "Orçamento enviado"})

@app.route("/api/avaliacoes", methods=["POST"])
@protegido
def avaliar(usuario):
    dados = request.json
    dados["usuario"] = usuario
    db.avaliacoes.insert_one(dados)
    return jsonify({"mensagem": "Avaliação registrada"})

@app.route("/api/vitrine", methods=["GET"])
@protegido
def vitrine(usuario):
    profissionais = list(db.profissionais.find({}))
    for p in profissionais:
        p["_id"] = str(p["_id"])
    return jsonify(profissionais)

# IA Clarice (Exemplo)
@app.route("/api/clarice", methods=["POST"])
@protegido
def clarice(usuario):
    pergunta = request.json.get("mensagem")
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": pergunta}]
    )
    texto = resposta.choices[0].message.content.strip()
    return jsonify({"resposta": texto})

# Inicializador
if __name__ == "__main__":
    app.run(debug=True)