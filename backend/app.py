from flask import Flask, jsonify
from flask_cors import CORS
from backend.database import init_db
from backend.routes.auth import auth_bp
from backend.routes.user import user_bp
from backend.routes.project import project_bp

app = Flask(__name__)
CORS(app)

# Inicializa DB em start (para SQLite/dev). Em produção, prefira migrations.
init_db()

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(project_bp)

# Healthcheck simples
@app.get("/health")
def health():
    return jsonify({"status": "ok"})