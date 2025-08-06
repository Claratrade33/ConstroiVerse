from flask import Flask
from flask_cors import CORS

from backend.config import SECRET_KEY
from backend.database import db  # noqa: F401 - initializes db connection

def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = SECRET_KEY

    @app.route("/")
    def index() -> dict:
        """Health-check endpoint."""
        return {"mensagem": "ConstroiVerse API funcionando 🎯"}

    # Import and register blueprints here to avoid circular imports
    from backend.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
