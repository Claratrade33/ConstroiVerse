from flask import Flask
from flask_cors import CORS

from backend.config import SECRET_KEY
from backend.database import db  # noqa: F401

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = SECRET_KEY

    @app.route("/")
    def index() -> dict:
        return {"mensagem": "ConstroiVerse API funcionando 🎯"}

    from backend.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from backend.routes.user import user_bp
    app.register_blueprint(user_bp)

    return app