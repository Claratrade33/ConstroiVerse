from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

# Inicializa app Flask
app = Flask(__name__)
CORS(app)

# Configurações do banco e segurança
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-constroiverse')

# Inicializa banco de dados
db = SQLAlchemy(app)

# Importa modelos (para criar as tabelas)
from models.user import User
from models.obra import Obra  # Novo modelo de obra

# Registra blueprints (rotas)
from controllers.auth_controller import auth_bp
from controllers.ia_controller import ia_bp
from controllers.obra_controller import obra_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(ia_bp, url_prefix='/ia')
app.register_blueprint(obra_bp, url_prefix='/obras')

# Rota inicial
@app.route('/')
def index():
    return jsonify({'msg': 'ConstroiVerse API rodando 🏗️'})

# Criação automática de tabelas no primeiro run
with app.app_context():
    db.create_all()

# Executa localmente
if __name__ == '__main__':
    app.run(debug=True)