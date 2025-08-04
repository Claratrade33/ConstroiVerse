from flask import Blueprint, jsonify, request
from database import db

corretor_controller = Blueprint('corretor_controller', __name__)
corretores_collection = db['corretores']
obras_collection = db['obras']

# Lista de obras disponíveis para corretores
@corretor_controller.route('/corretor/obras', methods=['GET'])
def listar_obras_disponiveis():
    obras = list(obras_collection.find({}, {'_id': 0}))
    return jsonify(obras)

# Cadastro ou atualização do corretor interessado
@corretor_controller.route('/corretor/interesse', methods=['POST'])
def registrar_interesse():
    dados = request.get_json()
    if 'corretor' not in dados or 'obra' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: corretor, obra'}), 400
    
    corretores_collection.insert_one(dados)
    return jsonify({'mensagem': 'Interesse registrado com sucesso'})