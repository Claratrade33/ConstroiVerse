from flask import Blueprint, jsonify, request
from database import db

representante_controller = Blueprint('representante_controller', __name__)
representantes_collection = db['representantes']
apresentacoes_collection = db['apresentacoes']
convites_collection = db['convites']

# Cadastrar representante
@representante_controller.route('/representantes', methods=['POST'])
def cadastrar_representante():
    dados = request.get_json()
    if 'nome' not in dados or 'produtos' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: nome, produtos'}), 400

    dados['pontuacao'] = 0
    representantes_collection.insert_one(dados)
    return jsonify({'mensagem': 'Representante cadastrado com sucesso'})

# Listar representantes
@representante_controller.route('/representantes', methods=['GET'])
def listar_representantes():
    reps = list(representantes_collection.find({}, {'_id': 0}))
    return jsonify(reps)

# Gerar currículo inteligente
@representante_controller.route('/representantes/<nome>/curriculo', methods=['POST'])
def gerar_curriculo(nome):
    dados = request.get_json()
    representante = representantes_collection.find_one({'nome': nome})
    
    if not representante:
        return jsonify({'erro': 'Representante não encontrado'}), 404

    curriculo = {
        'nome': nome,
        'produtos': dados.get('produtos', representante.get('produtos', [])),
        'resultados': dados.get('resultados', []),
        'apresentacao': f"{nome} representa os seguintes produtos: {', '.join(dados.get('produtos', []))}."
    }
    
    apresentacoes_collection.insert_one(curriculo)
    return jsonify({'mensagem': 'Currículo gerado com sucesso', 'curriculo': curriculo})

# Enviar currículo para fabricante ou loja
@representante_controller.route('/representantes/<nome>/enviar', methods=['POST'])
def enviar_apresentacao(nome):
    dados = request.get_json()
    destino = dados.get('destino')

    if not destino:
        return jsonify({'erro': 'Destino (fabricante ou loja) é obrigatório'}), 400

    apresentacao = apresentacoes_collection.find_one({'nome': nome})
    if not apresentacao:
        return jsonify({'erro': 'Nenhuma apresentação encontrada para esse representante'}), 404

    convite = {
        'representante': nome,
        'destino': destino,
        'status': 'Enviado',
        'mensagem': apresentacao.get('apresentacao')
    }
    convites_collection.insert_one(convite)
    return jsonify({'mensagem': f'Apresentação enviada para {destino}'})

# Ver convites recebidos (por destino)
@representante_controller.route('/convites/<destino>', methods=['GET'])
def convites_recebidos(destino):
    convites = list(convites_collection.find({'destino': destino}, {'_id': 0}))
    return jsonify(convites)