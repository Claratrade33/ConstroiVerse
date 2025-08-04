from flask import Blueprint, jsonify, request
from database import db

representantes_controller = Blueprint('representantes_controller', __name__)
representantes_collection = db['representantes']

# Listar representantes
@representantes_controller.route('/representantes', methods=['GET'])
def listar_representantes():
    representantes = list(representantes_collection.find({}, {'_id': 0}))
    return jsonify(representantes)

# Cadastrar representante
@representantes_controller.route('/representantes', methods=['POST'])
def cadastrar_representante():
    dados = request.get_json()
    if 'nome' not in dados or 'categoria' not in dados or 'marcas' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: nome, categoria, marcas'}), 400

    representantes_collection.insert_one(dados)
    return jsonify({'mensagem': 'Representante cadastrado com sucesso'})