from main import db
from datetime import datetime

class Orcamento(db.Model):
    __tablename__ = 'orcamentos'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    obra_id = db.Column(db.Integer, db.ForeignKey('obras.id'), nullable=True)

    descricao_input = db.Column(db.Text)       # o que o cliente digitou
    resposta_ia = db.Column(db.Text)           # JSON bruto da IA Clarice
    total_estimado = db.Column(db.String(50))  # valor aproximado
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Orcamento #{self.id} — Cliente {self.cliente_id}>'