from flask import Flask
from flask_cors import CORS

from backend.config import SECRET_KEY
from backend.database import db  # noqa: F401 - initializes db connection
from backend.controllers.auth_controller import auth_bp
from backend.controllers.perfil_controller import perfil_bp


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.register_blueprint(auth_bp)
    app.register_blueprint(perfil_bp)

    @app.route("/")
    def index() -> dict:
        """Health-check endpoint."""
        return {"mensagem": "ConstroiVerse API funcionando 🎯"}

    return app
