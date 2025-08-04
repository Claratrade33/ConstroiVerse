from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
import datetime
from config import SECRET_KEY
from models.user_model import users_db

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_db.get(username)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({'token': token, 'perfil': user['perfil']})