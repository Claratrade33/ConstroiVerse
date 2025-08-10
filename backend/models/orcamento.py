from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import relationship
from backend.database import Base

class Orcamento(Base):
    __tablename__ = "orcamentos"
    id = Column(Integer, primary_key=True, index=True)
    obra_id = Column(Integer, ForeignKey("obras.id"), nullable=False)
    descricao = Column(String(255), nullable=True)
    total = Column(Numeric(12, 2), nullable=False, default=0)
    status = Column(String(50), default="aberto", nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    obra = relationship("Obra", back_populates="orcamentos")