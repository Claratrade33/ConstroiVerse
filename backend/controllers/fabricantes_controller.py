from flask import Blueprint, jsonify, request
from database import db

fabricante_controller = Blueprint('fabricante_controller', __name__)
fabricantes_collection = db['fabricantes']

# Listar todos os fabricantes
@fabricante_controller.route('/fabricantes', methods=['GET'])
def listar_fabricantes():
    fabricantes = list(fabricantes_collection.find({}, {'_id': 0}))
    return jsonify(fabricantes)

# Cadastrar novo fabricante
@fabricante_controller.route('/fabricantes', methods=['POST'])
def cadastrar_fabricante():
    dados = request.get_json()
    if 'nome' not in dados or 'produtos' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: nome, produtos'}), 400

    fabricantes_collection.insert_one(dados)
    return jsonify({'mensagem': 'Fabricante cadastrado com sucesso'})

# Atualizar se vende direto para CNPJ
@fabricante_controller.route('/fabricantes/<nome>', methods=['PUT'])
def atualizar_venda_direta(nome):
    dados = request.get_json()
    vende_direto = dados.get('vende_direto', False)

    resultado = fabricantes_collection.update_one(
        {'nome': nome},
        {'$set': {'vende_direto': vende_direto}}
    )

    if resultado.matched_count == 0:
        return jsonify({'erro': 'Fabricante não encontrado'}), 404

    return jsonify({'mensagem': 'Atualização realizada com sucesso'})