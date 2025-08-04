from flask import Blueprint, jsonify, request
from database import db

perfil_controller = Blueprint('perfil_controller', __name__)
usuarios_collection = db['usuarios']

# Listar todos os usuários com perfis
@perfil_controller.route('/perfis', methods=['GET'])
def listar_perfis():
    usuarios = list(usuarios_collection.find({}, {'_id': 0}))
    return jsonify(usuarios)

# Cadastrar novo usuário com perfil
@perfil_controller.route('/perfis', methods=['POST'])
def cadastrar_perfil():
    dados = request.get_json()
    if not dados.get('nome') or not dados.get('perfil'):
        return jsonify({'erro': 'Campos obrigatórios: nome, perfil'}), 400

    usuarios_collection.insert_one(dados)
    return jsonify({'mensagem': 'Perfil cadastrado com sucesso'})

# Buscar usuários por tipo de perfil
@perfil_controller.route('/perfis/<perfil>', methods=['GET'])
def buscar_por_tipo(perfil):
    resultados = list(usuarios_collection.find({'perfil': perfil}, {'_id': 0}))
    return jsonify(resultados)