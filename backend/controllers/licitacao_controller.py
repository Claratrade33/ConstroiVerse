from flask import Blueprint, jsonify, request
from database import db

licitacoes_controller = Blueprint('licitacoes_controller', __name__)
licitacoes_collection = db['licitacoes']

# Listar licitações
@licitacoes_controller.route('/licitacoes', methods=['GET'])
def listar_licitacoes():
    licitacoes = list(licitacoes_collection.find({}, {'_id': 0}))
    return jsonify(licitacoes)

# Criar nova licitação
@licitacoes_controller.route('/licitacoes', methods=['POST'])
def criar_licitacao():
    dados = request.get_json()
    if not dados.get('nome') or not dados.get('status') or not dados.get('obra'):
        return jsonify({'erro': 'Campos obrigatórios: nome, status, obra'}), 400

    licitacoes_collection.insert_one(dados)
    return jsonify({'mensagem': 'Licitação criada com sucesso'})