from flask import Blueprint, jsonify, request
from database import db

profissional_controller = Blueprint('profissional_controller', __name__)
profissionais_collection = db['profissionais']

# Listar todos os profissionais
@profissional_controller.route('/profissionais', methods=['GET'])
def listar_profissionais():
    profissionais = list(profissionais_collection.find({}, {'_id': 0}))
    return jsonify(profissionais)

# Adicionar novo profissional
@profissional_controller.route('/profissionais', methods=['POST'])
def adicionar_profissional():
    dados = request.get_json()
    if not dados.get('nome') or not dados.get('especialidade'):
        return jsonify({'erro': 'Nome e especialidade são obrigatórios'}), 400

    profissionais_collection.insert_one(dados)
    return jsonify({'mensagem': 'Profissional cadastrado com sucesso'})