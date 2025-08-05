from flask import Flask
from flask_cors import CORS
from backend.database import db
from backend.config import SECRET_KEY
from backend.controllers.auth_controller import auth_bp
from backend.controllers.obra_controller import obra_bp
from backend.controllers.perfil_controller import perfil_bp
from backend.controllers.vitrine_controller import vitrine_bp
from backend.controllers.fabricante_controller import fabricante_bp
from backend.controllers.representante_controller import representante_bp
from backend.controllers.corretor_controller import corretor_bp
from backend.controllers.usuario_final_controller import usuario_final_bp

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = SECRET_KEY

# Rotas (Blueprints)
app.register_blueprint(auth_bp)
app.register_blueprint(obra_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(vitrine_bp)
app.register_blueprint(fabricante_bp)
app.register_blueprint(representante_bp)
app.register_blueprint(corretor_bp)
app.register_blueprint(usuario_final_bp)

# Inicial
@app.route('/')
def index():
    return {'mensagem': 'ConstroiVerse API funcionando 🎯'}

if __name__ == '__main__':
    app.run(debug=True)