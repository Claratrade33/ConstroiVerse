from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuração do banco e JWT
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-constroiverse')

db = SQLAlchemy(app)

# Importa modelos para criar as tabelas
from models.user import User

# Registra blueprints
from controllers.auth_controller import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

# Rota de teste
@app.route('/')
def index():
    return jsonify({'msg': 'API ConstroiVerse está ativa! 🏗️'})

# Cria as tabelas automaticamente
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)