from flask import Blueprint, request, jsonify
from models.user import User
from services.auth import generate_token, verify_password, hash_password
from main import db

auth_bp = Blueprint('auth', __name__)

# 📌 Registro de usuário
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    nome = data.get('nome')
    perfil = data.get('perfil')  # cliente, engenheiro, pedreiro, etc.

    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'Usuário já existe'}), 409

    user = User(
        email=email,
        senha=hash_password(senha),
        nome=nome,
        perfil=perfil
    )

    db.session.add(user)
    db.session.commit()
    token = generate_token(user)

    return jsonify({'msg': 'Usuário registrado com sucesso', 'token': token})

# 📌 Login de usuário
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(senha, user.senha):
        return jsonify({'msg': 'Credenciais inválidas'}), 401

    token = generate_token(user)
    return jsonify({'msg': 'Login realizado', 'token': token, 'perfil': user.perfil})