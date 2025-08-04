from flask import Blueprint, jsonify, request
from database import db

fabricante_controller = Blueprint('fabricante_controller', __name__)
fabricantes_collection = db['fabricantes']
orcamentos_collection = db['orcamentos']

# Listar fabricantes
@fabricante_controller.route('/fabricantes', methods=['GET'])
def listar_fabricantes():
    fabricantes = list(fabricantes_collection.find({}, {'_id': 0}))
    return jsonify(fabricantes)

# Cadastrar fabricante
@fabricante_controller.route('/fabricantes', methods=['POST'])
def cadastrar_fabricante():
    dados = request.get_json()
    if 'nome' not in dados or 'produtos' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: nome e produtos'}), 400

    dados['vende_direto'] = dados.get('vende_direto', False)
    fabricantes_collection.insert_one(dados)
    return jsonify({'mensagem': 'Fabricante cadastrado com sucesso'})

# Atualizar status de venda direta
@fabricante_controller.route('/fabricantes/<nome>/venda-direta', methods=['PUT'])
def atualizar_venda_direta(nome):
    dados = request.get_json()
    vende_direto = dados.get('vende_direto')

    if vende_direto is None:
        return jsonify({'erro': 'Campo vende_direto obrigatório'}), 400

    resultado = fabricantes_collection.update_one(
        {'nome': nome},
        {'$set': {'vende_direto': vende_direto}}
    )

    if resultado.matched_count == 0:
        return jsonify({'erro': 'Fabricante não encontrado'}), 404

    return jsonify({'mensagem': 'Status de venda direta atualizado'})

# Enviar orçamento para fabricante
@fabricante_controller.route('/fabricantes/<nome>/orcamentos', methods=['POST'])
def enviar_orcamento(nome):
    dados = request.get_json()
    fabricante = fabricantes_collection.find_one({'nome': nome})
    
    if not fabricante:
        return jsonify({'erro': 'Fabricante não encontrado'}), 404

    dados['fabricante'] = nome
    orcamentos_collection.insert_one(dados)
    return jsonify({'mensagem': 'Orçamento enviado com sucesso'})

# Ver orçamentos recebidos
@fabricante_controller.route('/fabricantes/<nome>/orcamentos', methods=['GET'])
def listar_orcamentos_recebidos(nome):
    orcamentos = list(orcamentos_collection.find({'fabricante': nome}, {'_id': 0}))
    return jsonify(orcamentos)