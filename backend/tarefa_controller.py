from flask import Blueprint, request, jsonify
from models.tarefa import Tarefa
from main import db
from datetime import datetime

tarefa_bp = Blueprint('tarefa', __name__)

# 🔹 Criar nova tarefa
@tarefa_bp.route('/tarefas', methods=['POST'])
def criar_tarefa():
    data = request.json
    nova = Tarefa(
        titulo=data.get('titulo'),
        descricao=data.get('descricao'),
        profissional_id=data.get('profissional_id'),
        obra_id=data.get('obra_id'),
        data_entrega=datetime.strptime(data.get('data_entrega'), '%Y-%m-%d') if data.get('data_entrega') else None,
        tipo=data.get('tipo')  # alvenaria, eletrica, etc.
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify({'msg': 'Tarefa criada com sucesso', 'tarefa_id': nova.id})

# 🔹 Listar tarefas por profissional (filtro por ID)
@tarefa_bp.route('/tarefas', methods=['GET'])
def listar_tarefas():
    profissional_id = request.args.get('profissional_id')
    if not profissional_id:
        return jsonify({'erro': 'ID do profissional é obrigatório'}), 400

    tarefas = Tarefa.query.filter_by(profissional_id=profissional_id).all()
    lista = []
    for t in tarefas:
        lista.append({
            'id': t.id,
            'titulo': t.titulo,
            'descricao': t.descricao,
            'status': t.status,
            'obra_id': t.obra_id,
            'tipo': t.tipo,
            'data_entrega': t.data_entrega.strftime('%Y-%m-%d') if t.data_entrega else None
        })
    return jsonify(lista)

# 🔹 Atualizar status de tarefa
@tarefa_bp.route('/tarefas/<int:tarefa_id>', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    data = request.json
    nova_descricao = data.get('descricao')
    novo_status = data.get('status')

    tarefa = Tarefa.query.get(tarefa_id)
    if not tarefa:
        return jsonify({'erro': 'Tarefa não encontrada'}), 404

    if nova_descricao:
        tarefa.descricao = nova_descricao
    if novo_status:
        tarefa.status = novo_status

    db.session.commit()
    return jsonify({'msg': 'Tarefa atualizada com sucesso'})