from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class Usuario(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    nome: str
    email: str
    senha: str
    tipo_usuario: str  # 'cliente', 'profissional', 'admin'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    def to_dict(self):
        return {
            "_id": str(self.id),
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha,
            "tipo_usuario": self.tipo_usuario,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class PerfilProfissional(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    usuario_id: PyObjectId
    profissao: str
    crea_cau: Optional[str]
    experiencia: Optional[int]
    especialidades: Optional[List[str]]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    def to_dict(self):
        return {
            "_id": str(self.id),
            "usuario_id": str(self.usuario_id),
            "profissao": self.profissao,
            "crea_cau": self.crea_cau,
            "experiencia": self.experiencia,
            "especialidades": self.especialidades,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class Material(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    nome: str
    unidade_medida: str
    categoria: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    def to_dict(self):
        return {
            "_id": str(self.id),
            "nome": self.nome,
            "unidade_medida": self.unidade_medida,
            "categoria": self.categoria,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class Transacao(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    type: str # 'income' ou 'expense'
    amount: float
    category: str
    description: Optional[str]
    date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    def to_dict(self):
        return {
            "_id": str(self.id),
            "user_id": str(self.user_id),
            "type": self.type,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class Projeto(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    nome_projeto: str
    descricao: Optional[str]
    profissional_id: PyObjectId
    cliente_id: PyObjectId
    tipo_projeto: str
    area_construida: float
    orcamento_estimado: float
    status: str
    data_inicio: Optional[datetime]
    data_fim_prevista: Optional[datetime]
    materiais_levantados: Optional[List[dict]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )

    def to_dict(self):
        return {
            "_id": str(self.id),
            "nome_projeto": self.nome_projeto,
            "descricao": self.descricao,
            "profissional_id": str(self.profissional_id),
            "cliente_id": str(self.cliente_id),
            "tipo_projeto": self.tipo_projeto,
            "area_construida": self.area_construida,
            "orcamento_estimado": self.orcamento_estimado,
            "status": self.status,
            "data_inicio": self.data_inicio,
            "data_fim_prevista": self.data_fim_prevista,
            "materiais_levantados": self.materiais_levantados,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
