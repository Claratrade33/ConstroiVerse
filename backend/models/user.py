from main import db

class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    perfil = db.Column(db.String(50), nullable=False)  # cliente, engenheiro, pedreiro, lojista, etc.

    def __repr__(self):
        return f'<User {self.email} - {self.perfil}>'