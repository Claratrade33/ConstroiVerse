from flask import Blueprint, jsonify, request
from database import db

representante_controller = Blueprint('representante_controller', __name__)
representantes_collection = db['representantes']

# Listar todos os representantes
@representante_controller.route('/representantes', methods=['GET'])
def listar_representantes():
    representantes = list(representantes_collection.find({}, {'_id': 0}))
    return jsonify(representantes)

# Cadastrar novo representante
@representante_controller.route('/representantes', methods=['POST'])
def cadastrar_representante():
    dados = request.get_json()
    if 'nome' not in dados or 'marcas' not in dados or 'regiao' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: nome, marcas, regiao'}), 400

    representantes_collection.insert_one(dados)
    return jsonify({'mensagem': 'Representante cadastrado com sucesso'})

# Atualizar portfólio
@representante_controller.route('/representantes/<nome>', methods=['PUT'])
def atualizar_portfolio(nome):
    dados = request.get_json()
    portfolio = dados.get('portfolio', [])

    resultado = representantes_collection.update_one(
        {'nome': nome},
        {'$set': {'portfolio': portfolio}}
    )

    if resultado.matched_count == 0:
        return jsonify({'erro': 'Representante não encontrado'}), 404

    return jsonify({'mensagem': 'Portfólio atualizado com sucesso'})

# Buscar representantes por marca e região
@representante_controller.route('/representantes/buscar', methods=['POST'])
def buscar_representantes():
    dados = request.get_json()
    marca = dados.get('marca')
    regiao = dados.get('regiao')

    query = {}
    if marca:
        query['marcas'] = marca
    if regiao:
        query['regiao'] = regiao

    resultados = list(representantes_collection.find(query, {'_id': 0}))
    return jsonify(resultados)