import os
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

# Conexão com o MongoDB
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.constroiverse
usuarios_collection = db['usuarios']

# Chave secreta para geração de token JWT
SECRET_KEY = os.getenv("SECRET_KEY", "CHAVESECRETA")

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    senha = data.get("senha")

    usuario = usuarios_collection.find_one({"username": username, "senha": senha})
    if usuario:
        token = jwt.encode({
            "user_id": str(usuario["_id"]),
            "username": usuario["username"],
            "perfil": usuario["perfil"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "status": "sucesso",
            "token": token,
            "username": usuario["username"],
            "perfil": usuario["perfil"]
        }), 200
    else:
        return jsonify({"status": "erro", "mensagem": "Usuário ou senha inválidos"}), 401

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    senha = data.get("senha")
    perfil = data.get("perfil", "cliente")

    if usuarios_collection.find_one({"username": username}):
        return jsonify({"status": "erro", "mensagem": "Usuário já existe"}), 400

    usuarios_collection.insert_one({
        "username": username,
        "senha": senha,
        "perfil": perfil
    })

    return jsonify({"status": "sucesso", "mensagem": "Usuário registrado com sucesso"}), 201