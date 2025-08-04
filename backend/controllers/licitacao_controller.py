from flask import Blueprint, jsonify, request
from database import db

licitacao_controller = Blueprint('licitacao_controller', __name__)
licitacoes_collection = db['licitacoes']

# Listar todas as licitações
@licitacao_controller.route('/licitacoes', methods=['GET'])
def listar_licitacoes():
    licitacoes = list(licitacoes_collection.find({}, {'_id': 0}))
    return jsonify(licitacoes)

# Adicionar nova licitação
@licitacao_controller.route('/licitacoes', methods=['POST'])
def adicionar_licitacao():
    dados = request.get_json()
    if not dados.get('nome') or not dados.get('obra'):
        return jsonify({'erro': 'Nome e obra são obrigatórios'}), 400

    licitacoes_collection.insert_one(dados)
    return jsonify({'mensagem': 'Licitação cadastrada com sucesso'})