import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Inicialização do Flask
app = Flask(__name__)
CORS(app)

# Configurações básicas
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'segredo-padrao')

# Importação dos blueprints
from backend.controllers.auth_controller import auth_bp
from backend.controllers.obra_controller import obra_bp
from backend.controllers.ia_controller import ia_bp
from backend.controllers.orcamento_controller import orcamento_bp
from backend.controllers.perfil_controller import perfil_bp
from backend.controllers.painel_controller import painel_bp
from backend.controllers.profissional_controller import profissional_bp
from backend.controllers.vitrine_controller import vitrine_bp

# Registro dos blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(obra_bp)
app.register_blueprint(ia_bp)
app.register_blueprint(orcamento_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(painel_bp)
app.register_blueprint(profissional_bp)
app.register_blueprint(vitrine_bp)

# Rota inicial
@app.route('/')
def index():
    return {'status': 'ConstroiVerse ativo com sucesso'}

# Execução no Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)