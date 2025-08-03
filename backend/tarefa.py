from main import db
from datetime import datetime

class Tarefa(db.Model):
    __tablename__ = 'tarefas'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default="pendente")  # pendente, em andamento, concluída

    profissional_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    obra_id = db.Column(db.Integer, db.ForeignKey('obras.id'), nullable=False)

    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_entrega = db.Column(db.DateTime, nullable=True)

    tipo = db.Column(db.String(30))  # Ex: 'alvenaria', 'eletrica', 'hidraulica'

    def __repr__(self):
        return f'<Tarefa {self.titulo} — {self.status}>'