from flask import Blueprint, jsonify, request
from database import db

vitrine_controller = Blueprint('vitrine_controller', __name__)
profissionais_collection = db['profissionais']

# Exibir todos os profissionais disponíveis na vitrine
@vitrine_controller.route('/vitrine', methods=['GET'])
def listar_profissionais():
    profissionais = list(profissionais_collection.find({}, {'_id': 0}))
    return jsonify(profissionais)

# Filtrar profissionais por especialidade e/ou região
@vitrine_controller.route('/vitrine/buscar', methods=['GET'])
def buscar_profissionais():
    especialidade = request.args.get('especialidade')
    regiao = request.args.get('regiao')

    query = {}
    if especialidade:
        query['especialidade'] = especialidade
    if regiao:
        query['regiao'] = regiao

    resultados = list(profissionais_collection.find(query, {'_id': 0}))
    return jsonify(resultados)

# Cadastrar novo profissional na vitrine
@vitrine_controller.route('/vitrine', methods=['POST'])
def cadastrar_profissional():
    dados = request.get_json()
    if not dados.get('nome') or not dados.get('especialidade'):
        return jsonify({'erro': 'Campos obrigatórios: nome, especialidade'}), 400

    profissionais_collection.insert_one(dados)
    return jsonify({'mensagem': 'Profissional adicionado à vitrine com sucesso'})