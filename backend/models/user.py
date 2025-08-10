from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.database import Base

class Obra(Base):
    __tablename__ = "obras"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(180), nullable=False)
    endereco = Column(String(255), nullable=True)
    status = Column(String(50), default="planejamento", nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="obras")
    orcamentos = relationship("Orcamento", back_populates="obra", cascade="all,delete-orphan")