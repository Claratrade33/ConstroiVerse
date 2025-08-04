import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient

# Load .env
load_dotenv()

# Configuração Flask
app = Flask(__name__, template_folder='frontend/painel', static_folder='frontend/static')
CORS(app)

# Conexão MongoDB
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['constroiverse']

# Blueprints
from backend.controllers.auth_controller import auth_bp
from backend.controllers.obra_controller import obra_bp
from backend.controllers.perfil_controller import perfil_bp
from backend.controllers.vitrine_controller import vitrine_bp
from backend.controllers.fabricante_controller import fabricante_bp
from backend.controllers.representante_controller import representante_bp

# Registrar rotas
app.register_blueprint(auth_bp)
app.register_blueprint(obra_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(vitrine_bp)
app.register_blueprint(fabricante_bp)
app.register_blueprint(representante_bp)

# Rota principal (opcional, pode remover se usar SPA)
@app.route('/')
def index():
    return jsonify({"status": "API ConstroiVerse ativa"})

# Rodar no Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)