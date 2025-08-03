from flask import Blueprint, request, jsonify
from models.obra import Obra
from models.user import User
from main import db
from datetime import datetime

obra_bp = Blueprint('obra', __name__)

# 🔹 Criar nova obra
@obra_bp.route('/obras', methods=['POST'])
def criar_obra():
    data = request.json
    nova_obra = Obra(
        titulo=data.get('titulo'),
        descricao=data.get('descricao'),
        cliente_id=data.get('cliente_id'),
        data_previsao_entrega=datetime.strptime(data.get('data_previsao_entrega'), '%Y-%m-%d'),
        profissionais=','.join(data.get('profissionais', []))  # lista de IDs
    )
    db.session.add(nova_obra)
    db.session.commit()
    return jsonify({'msg': 'Obra criada com sucesso', 'obra_id': nova_obra.id})

# 🔹 Listar todas as obras
@obra_bp.route('/obras', methods=['GET'])
def listar_obras():
    obras = Obra.query.all()
    lista = []
    for obra in obras:
        lista.append({
            'id': obra.id,
            'titulo': obra.titulo,
            'status_geral': obra.status_geral,
            'fundacao': obra.etapa_fundacao,
            'alvenaria': obra.etapa_alvenaria,
            'eletrica': obra.etapa_eletrica,
            'hidraulica': obra.etapa_hidraulica,
            'acabamento': obra.etapa_acabamento,
            'previsao_entrega': obra.data_previsao_entrega.strftime('%Y-%m-%d') if obra.data_previsao_entrega else None
        })
    return jsonify(lista)

# 🔹 Ver detalhes de uma obra específica
@obra_bp.route('/obras/<int:obra_id>', methods=['GET'])
def detalhes_obra(obra_id):
    obra = Obra.query.get(obra_id)
    if not obra:
        return jsonify({'erro': 'Obra não encontrada'}), 404

    return jsonify({
        'id': obra.id,
        'titulo': obra.titulo,
        'descricao': obra.descricao,
        'cliente_id': obra.cliente_id,
        'status_geral': obra.status_geral,
        'etapas': {
            'fundacao': obra.etapa_fundacao,
            'alvenaria': obra.etapa_alvenaria,
            'eletrica': obra.etapa_eletrica,
            'hidraulica': obra.etapa_hidraulica,
            'acabamento': obra.etapa_acabamento
        },
        'profissionais': obra.profissionais.split(',') if obra.profissionais else [],
        'inicio': obra.data_inicio.strftime('%Y-%m-%d'),
        'previsao_entrega': obra.data_previsao_entrega.strftime('%Y-%m-%d') if obra.data_previsao_entrega else None
    })

# 🔹 Atualizar etapa específica da obra
@obra_bp.route('/obras/<int:obra_id>/etapa', methods=['PUT'])
def atualizar_etapa(obra_id):
    data = request.json
    etapa = data.get('etapa')
    status = data.get('status')

    obra = Obra.query.get(obra_id)
    if not obra:
        return jsonify({'erro': 'Obra não encontrada'}), 404

    if etapa == 'fundacao': obra.etapa_fundacao = status
    elif etapa == 'alvenaria': obra.etapa_alvenaria = status
    elif etapa == 'eletrica': obra.etapa_eletrica = status
    elif etapa == 'hidraulica': obra.etapa_hidraulica = status
    elif etapa == 'acabamento': obra.etapa_acabamento = status
    else:
        return jsonify({'erro': 'Etapa inválida'}), 400

    db.session.commit()
    return jsonify({'msg': f'Etapa "{etapa}" atualizada para "{status}"'})