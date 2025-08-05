from flask import Flask
from flask_cors import CORS
from backend.database import db
from backend.config import SECRET_KEY

# Importando os blueprints
from backend.controllers.auth_controller import auth_bp
from backend.controllers.documento_controller import documento_bp
from backend.controllers.fabricantes_controller import fabricantes_bp
from backend.controllers.ia_controller import ia_bp
from backend.controllers.licitacao_controller import licitacao_bp
from backend.controllers.materiais_controller import materiais_bp
from backend.controllers.obra_controller import obra_bp
from backend.controllers.orcamento_controller import orcamento_bp
from backend.controllers.profissional_controller import profissional_bp
from backend.controllers.representantes_controller import representantes_bp
from backend.controllers.corretor_controller import corretor_bp
from backend.controllers.cliente_controller import cliente_bp
from backend.controllers.vitrine_controller import vitrine_bp

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = SECRET_KEY

# Registrando os blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(documento_bp)
app.register_blueprint(fabricantes_bp)
app.register_blueprint(ia_bp)
app.register_blueprint(licitacao_bp)
app.register_blueprint(materiais_bp)
app.register_blueprint(obra_bp)
app.register_blueprint(orcamento_bp)
app.register_blueprint(profissional_bp)
app.register_blueprint(representantes_bp)
app.register_blueprint(corretor_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(vitrine_bp)

@app.route('/')
def index():
    return {"status": "API ConstroiVerse online"}

if __name__ == '__main__':
    app.run(debug=True)