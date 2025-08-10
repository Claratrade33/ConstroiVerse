from flask import Flask
from flask_cors import CORS
from backend.routes.auth import auth_bp
# from backend.routes.user import user_bp
# from backend.routes.project import project_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
# app.register_blueprint(user_bp)
# app.register_blueprint(project_bp)