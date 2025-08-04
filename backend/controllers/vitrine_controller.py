from flask import Blueprint, jsonify, request
from database import db

vitrine_controller = Blueprint('vitrine_controller', __name__)
profissionais_collection = db['profissionais']

# Listar todos os profissionais da vitrine
@vitrine_controller.route('/vitrine', methods=['GET'])
def listar_vitrine():
    profissionais = list(profissionais_collection.find({}, {'_id': 0}))
    return jsonify(profissionais)

# Cadastrar profissional na vitrine
@vitrine_controller.route('/vitrine', methods=['POST'])
def cadastrar_profissional():
    dados = request.get_json()
    campos_obrigatorios = ['nome', 'especialidade', 'regiao', 'pontuacao']

    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({'erro': f'Campos obrigatórios: {", ".join(campos_obrigatorios)}'}), 400

    profissionais_collection.insert_one(dados)
    return jsonify({'mensagem': 'Profissional adicionado à vitrine com sucesso'})

# Filtrar por especialidade, região ou pontuação mínima
@vitrine_controller.route('/vitrine/buscar', methods=['POST'])
def buscar_profissionais():
    dados = request.get_json()
    filtro = {}

    if 'especialidade' in dados:
        filtro['especialidade'] = dados['especialidade']
    if 'regiao' in dados:
        filtro['regiao'] = dados['regiao']
    if 'pontuacao_minima' in dados:
        filtro['pontuacao'] = {'$gte': dados['pontuacao_minima']}

    resultados = list(profissionais_collection.find(filtro, {'_id': 0}))
    return jsonify(resultados)

# Atualizar pontuação do profissional
@vitrine_controller.route('/vitrine/<nome>/pontuacao', methods=['PUT'])
def atualizar_pontuacao(nome):
    dados = request.get_json()
    nova_pontuacao = dados.get('pontuacao')

    if nova_pontuacao is None:
        return jsonify({'erro': 'Informe a nova pontuação'}), 400

    resultado = profissionais_collection.update_one(
        {'nome': nome},
        {'$set': {'pontuacao': nova_pontuacao}}
    )

    if resultado.matched_count == 0:
        return jsonify({'erro': 'Profissional não encontrado'}), 404

    return jsonify({'mensagem': 'Pontuação atualizada com sucesso'})