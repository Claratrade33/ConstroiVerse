# -*- coding: utf-8 -*-
"""
    ConstroiVerse API
    ~~~~~~

    A API para a plataforma ConstroiVerse, que conecta clientes a profissionais
    da construção civil.
"""

import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

from .routes.user import user_bp
from .routes.projetos import projetos_bp
from .routes.financial import financial_bp


app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'construiverse#2025$SECRET'

# Habilitar CORS para permitir requisições do frontend
CORS(app)

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(projetos_bp, url_prefix='/api')
app.register_blueprint(financial_bp, url_prefix='/api')


@app.route("/api/status", methods=["GET"])
def status():
    """Endpoint para verificar se a API está funcionando"""
    return {
        'status': 'ConstroiVerse API está funcionando!',
        'version': '2.0.0',
        'endpoints': [
            '/api/projetos',
            '/api/orcamentos',
            '/api/ia',
            '/api/users',
            '/api/financeiro',
            '/api/vitrine'
        ]
    }

@app.route("/api/profissoes", methods=["GET"])
def get_profissoes():
    """Endpoint para obter lista de profissões da construção civil"""
    from src.services.vitrine_service import VitrineService
    service = VitrineService()
    return jsonify(service.get_profissoes_por_categoria()), 200

@app.route("/api/especialidades/<profissao>", methods=["GET"])
def get_especialidades(profissao):
    """Endpoint para obter especialidades de uma profissão"""
    from src.services.vitrine_service import VitrineService
    service = VitrineService()
    especialidades = service.get_especialidades_profissao(profissao)
    return jsonify({'especialidades': especialidades}), 200

@app.route("/api/faixa-preco/<profissao>", methods=["GET"])
def get_faixa_preco(profissao):
    """Endpoint para obter faixa de preço de uma profissão"""
    from src.services.vitrine_service import VitrineService
    service = VitrineService()
    faixa = service.get_faixa_preco_profissao(profissao)
    return jsonify(faixa), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
