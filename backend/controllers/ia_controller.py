from flask import Blueprint, request, jsonify
from services.clarice import gerar_orcamento

ia_bp = Blueprint('ia', __name__)

# 🔮 Rota para conversar com a Clarice
@ia_bp.route('/chat', methods=['POST'])
def chat_clarice():
    data = request.json
    descricao = data.get('descricao')

    if not descricao:
        return jsonify({'erro': 'Descrição da obra é obrigatória'}), 400

    resposta = gerar_orcamento(descricao)

    # Se a IA retornou um JSON como string, tenta converter
    if isinstance(resposta, str):
        try:
            import json
            return jsonify(json.loads(resposta))
        except:
            return jsonify({'resposta': resposta})
    else:
        return jsonify(resposta)