from main import db
from datetime import datetime

class Obra(db.Model):
    __tablename__ = 'obras'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))  # relação com o cliente

    status_geral = db.Column(db.String(50), default="planejamento")  # andamento geral
    etapa_fundacao = db.Column(db.String(20), default="pendente")
    etapa_alvenaria = db.Column(db.String(20), default="pendente")
    etapa_eletrica = db.Column(db.String(20), default="pendente")
    etapa_hidraulica = db.Column(db.String(20), default="pendente")
    etapa_acabamento = db.Column(db.String(20), default="pendente")

    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_previsao_entrega = db.Column(db.DateTime, nullable=True)

    profissionais = db.Column(db.Text)  # lista de IDs separados por vírgula (ex: pedreiro, engenheiro)

    def __repr__(self):
        return f'<Obra {self.titulo} — Status: {self.status_geral}>'