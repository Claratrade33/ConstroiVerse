from flask import Blueprint, jsonify, request
from database import db

perfil_controller = Blueprint('perfil_controller', __name__)
usuarios_collection = db['usuarios']

# Retorna o painel correto de acordo com o perfil
@perfil_controller.route('/perfil/<usuario>', methods=['GET'])
def obter_painel(usuario):
    usuario_data = usuarios_collection.find_one({'usuario': usuario})

    if not usuario_data:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

    perfil = usuario_data.get('perfil')

    rotas = {
        'arquiteto': '/painel_arquiteto',
        'engenheiro': '/painel_engenheiro',
        'loja': '/painel_loja',
        'fabricante': '/painel_fabricante',
        'representante': '/painel_representante',
        'corretor': '/painel_corretor',
        'mestre': '/painel_mestre',
        'pedreiro': '/painel_pedreiro',
        'eletricista': '/painel_eletricista',
        'encanador': '/painel_encanador',
        'cliente': '/painel_cliente',
        'construtora': '/painel_construtora'
    }

    rota_painel = rotas.get(perfil)

    if not rota_painel:
        return jsonify({'erro': 'Perfil não reconhecido'}), 400

    return jsonify({'painel': rota_painel})