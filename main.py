from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import openai
import jwt
import datetime
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Caminhos absolutos para compatibilidade com Render
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'frontend', 'painel')
STATIC_DIR = os.path.join(BASE_DIR, 'frontend')

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATE_DIR)
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

# Rota inicial
@app.route('/')
def home():
    return render_template('painel_construtora.html')

# Rota dinâmica dos painéis
@app.route('/painel/<perfil>')
def render_painel(perfil):
    try:
        return render_template(f'painel_{perfil}.html')
    except:
        return f"Painel '{perfil}' não encontrado.", 404

# API - Status
@app.route("/api")
def index():
    return jsonify({"status": "ConstroiVerse API está rodando 🏗️"}), 200

# API - Login
@app.route("/api/login", methods=["POST"])
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

# API - Registro
@app.route("/api/register", methods=["POST"])
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

# API - IA Clarice
@app.route("/api/ia", methods=["POST"])
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

# API - Perfil
@app.route("/api/usuario", methods=["GET"])
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

# Execução
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port, debug=True)