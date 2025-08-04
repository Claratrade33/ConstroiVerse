import os
from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

# Inicializa o app Flask
app = Flask(__name__)
CORS(app)

# Configurações
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['constroiverse']

# Banco disponível globalmente
app.db = db

# Importa e registra as rotas dos controllers
from controllers.auth_controller import auth_bp
from controllers.ia_controller import ia_bp
from controllers.obra_controller import obra_bp
from controllers.orcamento_controller import orcamento_bp

# Registra blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(ia_bp, url_prefix='/api/ia')
app.register_blueprint(obra_bp, url_prefix='/api/obras')
app.register_blueprint(orcamento_bp, url_prefix='/api/orcamentos')

# Rota raiz de status
@app.route('/')
def status():
    return jsonify({"status": "API ConstroiVerse ativa com sucesso 🚀"})

# Inicia o servidor
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)