from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import openai
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Variáveis de ambiente
SECRET_KEY = os.getenv('SECRET_KEY')
MONGO_URI = os.getenv('MONGO_URI')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Configurações
app.config['SECRET_KEY'] = SECRET_KEY
openai.api_key = OPENAI_API_KEY

# Conexão com MongoDB
client = MongoClient(MONGO_URI)
db = client['constroiverse']
usuarios_collection = db['usuarios']
mensagens_collection = db['mensagens']

# Rota de teste
@app.route("/")
def index():
    return jsonify({"status": "ConstroiVerse API está rodando 🏗️"}), 200

# Autenticação
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = usuarios_collection.find_one({
        "username": data["username"],
        "password": data["password"]
    })
    if user:
        token = jwt.encode({
            "user_id": str(user["_id"]),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401

# Cadastro
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if usuarios_collection.find_one({"username": data["username"]}):
        return jsonify({"error": "Usuário já existe"}), 400
    usuarios_collection.insert_one({
        "username": data["username"],
        "password": data["password"],
        "perfil": data.get("perfil", "cliente")
    })
    return jsonify({"message": "Cadastro realizado com sucesso!"}), 201

# IA Clarice: responder perguntas
@app.route("/ia", methods=["POST"])
def ia_clarice():
    data = request.json
    prompt = data.get("mensagem", "")
    if not prompt:
        return jsonify({"erro": "Mensagem ausente"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é a Clarice, uma assistente inteligente especializada em construção civil. Responda com clareza e agilidade."},
                {"role": "user", "content": prompt}
            ]
        )
        resposta = response['choices'][0]['message']['content']
        mensagens_collection.insert_one({
            "entrada": prompt,
            "resposta": resposta,
            "data": datetime.datetime.utcnow()
        })
        return jsonify({"resposta": resposta})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota protegida de exemplo
@app.route("/usuario", methods=["GET"])
def get_usuario():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token ausente"}), 401
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = usuarios_collection.find_one({"_id": decoded["user_id"]})
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        return jsonify({"username": user["username"], "perfil": user.get("perfil", "cliente")})
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except Exception:
        return jsonify({"error": "Token inválido"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)