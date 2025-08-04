import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient

# Carregar variáveis de ambiente
load_dotenv()

# Configuração Flask
app = Flask(__name__)
CORS(app)

# Conexão MongoDB
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['constroiverse']

# IMPORTS dos BLUEPRINTS - NOMES EXATOS DOS SEUS ARQUIVOS
from backend.controllers.auth_controller import auth_bp
from backend.controllers.corretor_controller import corretor_bp
from backend.controllers.documento_controller import documento_bp
from backend.controllers.fabricantes_controller import fabricantes_bp
from backend.controllers.ia_controller import ia_bp
from backend.controllers.licitacao_controller import licitacao_bp
from backend.controllers.materiais_controller import materiais_bp
from backend.controllers.obra_controller import obra_bp
from backend.controllers.orcamento_controller import orcamento_bp
from backend.controllers.perfil_controller import perfil_bp
from backend.controllers.profissional_controller import profissional_bp
from backend.controllers.representantes_controller import representantes_bp
from backend.controllers.vitrine_controller import vitrine_bp

# REGISTRO dos BLUEPRINTS
app.register_blueprint(auth_bp)
app.register_blueprint(corretor_bp)
app.register_blueprint(documento_bp)
app.register_blueprint(fabricantes_bp)
app.register_blueprint(ia_bp)
app.register_blueprint(licitacao_bp)
app.register_blueprint(materiais_bp)
app.register_blueprint(obra_bp)
app.register_blueprint(orcamento_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(profissional_bp)
app.register_blueprint(representantes_bp)
app.register_blueprint(vitrine_bp)

# Rota principal (teste)
@app.route('/')
def index():
    return jsonify({"status": "API ConstroiVerse rodando 🔥"})

# Inicializar
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)