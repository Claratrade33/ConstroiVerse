import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient

# Carregar variáveis de ambiente (.env)
load_dotenv()

# Configuração do Flask
app = Flask(
    __name__,
    template_folder='frontend/painel',  # Se precisar de templates HTML
    static_folder='frontend/static'     # Para arquivos JS/CSS
)
CORS(app)

# Conexão com MongoDB
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['constroiverse']

# Deixe isso disponível para os outros módulos
app.db = db

# IMPORTAÇÃO E REGISTRO DOS BLUEPRINTS

from backend.controllers.authController import auth_bp
from backend.controllers.obra_controller import obra_bp
from backend.controllers.perfil_controller import perfil_bp
from backend.controllers.vitrine_controller import vitrine_bp
from backend.controllers.fabricante_controller import fabricante_bp
from backend.controllers.representante_controller import representante_bp
from backend.controllers.deliveryController import delivery_bp
from backend.controllers.evaluationController import evaluation_bp
from backend.controllers.logisticaController import logistica_bp
from backend.controllers.quoteController import quote_bp
from backend.controllers.reportController import report_bp
from backend.controllers.stockController import stock_bp
from backend.controllers.taskController import task_bp

# Registro dos blueprints (rotas)
app.register_blueprint(auth_bp)
app.register_blueprint(obra_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(vitrine_bp)
app.register_blueprint(fabricante_bp)
app.register_blueprint(representante_bp)
app.register_blueprint(delivery_bp)
app.register_blueprint(evaluation_bp)
app.register_blueprint(logistica_bp)
app.register_blueprint(quote_bp)
app.register_blueprint(report_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(task_bp)

# Rota de status (opcional)
@app.route('/')
def index():
    return jsonify({"status": "API ConstroiVerse ativa"})

# Rodar servidor (para dev/local)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)