from flask import Flask
from flask_cors import CORS
from backend.database import db
from config import MONGO_URI
from backend.controllers.auth_controller import auth_bp
from backend.controllers.obra_controller import obra_controller
from backend.controllers.perfil_controller import perfil_controller
from backend.controllers.vitrine_controller import vitrine_controller
from backend.controllers.fabricante_controller import fabricante_controller
from backend.controllers.representante_controller import representante_controller
from backend.controllers.loja_controller import loja_controller
from backend.controllers.arquiteto_controller import arquiteto_controller
from backend.controllers.engenheiro_controller import engenheiro_controller
from backend.controllers.pedreiro_controller import pedreiro_controller
from backend.controllers.eletricista_controller import eletricista_controller
from backend.controllers.encanador_controller import encanador_controller
from backend.controllers.mestre_obra_controller import mestre_obra_controller
from backend.controllers.cliente_controller import cliente_controller
from backend.controllers.corretor_controller import corretor_controller

app = Flask(__name__)
CORS(app)

# Configura o MongoDB
app.config["MONGO_URI"] = MONGO_URI
db.init_app(app)

# Blueprints registrados
app.register_blueprint(auth_bp)
app.register_blueprint(obra_controller)
app.register_blueprint(perfil_controller)
app.register_blueprint(vitrine_controller)
app.register_blueprint(fabricante_controller)
app.register_blueprint(representante_controller)
app.register_blueprint(loja_controller)
app.register_blueprint(arquiteto_controller)
app.register_blueprint(engenheiro_controller)
app.register_blueprint(pedreiro_controller)
app.register_blueprint(eletricista_controller)
app.register_blueprint(encanador_controller)
app.register_blueprint(mestre_obra_controller)
app.register_blueprint(cliente_controller)
app.register_blueprint(corretor_controller)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)