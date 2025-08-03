from flask import Blueprint, request, jsonify
from models.orcamento import Orcamento
from main import db
from datetime import datetime

orcamento_bp = Blueprint('orcamento', __name__)

# 🔹 Salvar novo orçamento
@orcamento_bp.route('/orcamentos', methods=['POST'])
def salvar_orcamento():
    data = request.json

    novo = Orcamento(
        cliente_id=data.get('cliente_id'),
        obra_id=data.get('obra_id'),
        descricao_input=data.get('descricao_input'),
        resposta_ia=data.get('resposta_ia'),
        total_estimado=data.get('total_estimado')
    )

    db.session.add(novo)
    db.session.commit()
    return jsonify({'msg': 'Orçamento salvo com sucesso', 'orcamento_id': novo.id})

# 🔹 Listar orçamentos de um cliente
@orcamento_bp.route('/orcamentos', methods=['GET'])
def listar_orcamentos():
    cliente_id = request.args.get('cliente_id')
    if not cliente_id:
        return jsonify({'erro': 'ID do cliente é obrigatório'}), 400

    orcamentos = Orcamento.query.filter_by(cliente_id=cliente_id).all()
    lista = []
    for o in orcamentos:
        lista.append({
            'id': o.id,
            'descricao': o.descricao_input,
            'total_estimado': o.total_estimado,
            'data': o.data_criacao.strftime('%Y-%m-%d'),
        })
    return jsonify(lista)

# 🔹 Ver orçamento específico
@orcamento_bp.route('/orcamentos/<int:orcamento_id>', methods=['GET'])
def detalhe_orcamento(orcamento_id):
    o = Orcamento.query.get(orcamento_id)
    if not o:
        return jsonify({'erro': 'Orçamento não encontrado'}), 404

    return jsonify({
        'id': o.id,
        'descricao': o.descricao_input,
        'resposta_ia': o.resposta_ia,
        'total_estimado': o.total_estimado,
        'data': o.data_criacao.strftime('%Y-%m-%d'),
    })