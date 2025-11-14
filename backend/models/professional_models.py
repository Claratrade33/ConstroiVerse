"""
Modelos MongoDB para Vitrine de Profissionais, Gestão Financeira, Comunicação Interna e Módulo Imobiliário
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema):
        schema.update(type="string")
        return schema


class ProfessionalProfile(BaseModel):
    """Modelo para Perfil de Profissional (Vitrine de Profissionais)"""
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId  # Referência ao usuário
    name: str
    email: EmailStr
    phone: str
    profession: str  # ex: "Pedreiro", "Eletricista", "Arquiteto"
    bio: Optional[str] = None
    location: str  # Cidade/Região
    experience_years: int = 0
    profile_image_url: Optional[str] = None
    portfolio_images: List[str] = []
    
    # Avaliações
    average_rating: float = 0.0
    total_reviews: int = 0
    reviews: List[Dict[str, Any]] = []
    
    # Status
    is_available: bool = True
    specialties: List[str] = []  # ex: ["Fundação", "Cerâmica", "Pintura"]
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "name": "João Silva",
                "email": "joao@example.com",
                "phone": "+55 11 98765-4321",
                "profession": "Pedreiro",
                "location": "São Paulo, SP",
                "experience_years": 10,
                "specialties": ["Fundação", "Alvenaria"]
            }
        }


class FinancialRecord(BaseModel):
    """Modelo para Registro Financeiro (Gestão Financeira)"""
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId  # Referência ao usuário
    project_id: Optional[PyObjectId] = None  # Referência ao projeto
    
    type: str  # "income" ou "expense"
    category: str  # ex: "salary", "material", "equipment", "service"
    description: str
    amount: float
    currency: str = "BRL"
    
    date: datetime = Field(default_factory=datetime.utcnow)
    payment_method: Optional[str] = None  # "cash", "check", "transfer", "credit_card"
    status: str = "pending"  # "pending", "completed", "cancelled"
    
    # Informações adicionais
    invoice_number: Optional[str] = None
    notes: Optional[str] = None
    attachments: List[str] = []  # URLs de documentos
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class Message(BaseModel):
    """Modelo para Mensagens de Comunicação Interna"""
    id: Optional[PyObjectId] = Field(alias="_id")
    sender_id: PyObjectId
    recipient_id: PyObjectId
    
    subject: Optional[str] = None  # Para e-mails formais
    content: str
    message_type: str = "chat"  # "chat" ou "email"
    
    is_read: bool = False
    read_at: Optional[datetime] = None
    
    attachments: List[str] = []  # URLs de arquivos
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class RealEstateProperty(BaseModel):
    """Modelo para Propriedade Imobiliária (Módulo Imobiliário)"""
    id: Optional[PyObjectId] = Field(alias="_id")
    owner_id: PyObjectId  # Referência ao proprietário
    
    title: str
    description: str
    property_type: str  # "house", "apartment", "commercial", "land"
    address: str
    city: str
    state: str
    zip_code: str
    
    # Características
    area_sqm: float
    bedrooms: int = 0
    bathrooms: int = 0
    parking_spaces: int = 0
    
    # Preço e disponibilidade
    price: float
    currency: str = "BRL"
    status: str = "available"  # "available", "sold", "rented"
    
    # Imagens
    images: List[str] = []
    
    # Agentes/Corretores
    assigned_brokers: List[PyObjectId] = []
    
    # Dados da obra (se for uma obra em andamento)
    is_construction: bool = False
    construction_status: Optional[str] = None  # "planning", "foundation", "structure", "finishing", "completed"
    estimated_completion: Optional[datetime] = None
    professionals_involved: List[PyObjectId] = []  # Referências a profissionais
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class BrokerProfile(BaseModel):
    """Modelo para Perfil de Corretor (Módulo Imobiliário)"""
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    
    name: str
    email: EmailStr
    phone: str
    creci: str  # Número do CRECI (Conselho Regional de Corretores de Imóveis)
    
    company: Optional[str] = None
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    
    # Avaliações
    average_rating: float = 0.0
    total_reviews: int = 0
    
    # Propriedades gerenciadas
    managed_properties: List[PyObjectId] = []
    
    # Status
    is_active: bool = True
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class SmartStoreInteraction(BaseModel):
    """Modelo para Interações da SmartStore IA"""
    id: Optional[PyObjectId] = Field(alias="_id")
    property_id: PyObjectId
    
    visitor_name: str
    visitor_email: EmailStr
    visitor_phone: Optional[str] = None
    
    interaction_type: str  # "inquiry", "visit", "purchase_interest"
    message: str
    
    # Dados coletados pela IA
    ai_response: Optional[str] = None
    ai_sentiment: Optional[str] = None  # "positive", "neutral", "negative"
    
    # Follow-up
    follow_up_status: str = "pending"  # "pending", "contacted", "converted"
    assigned_broker: Optional[PyObjectId] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class Task(BaseModel):
    """Modelo para Tarefas de Obra (Gestão de Pessoal)"""
    id: Optional[PyObjectId] = Field(alias="_id")
    project_id: PyObjectId
    
    title: str
    description: str
    category: str  # "foundation", "ceramic", "painting", etc.
    
    # Profissionais atribuídos
    assigned_professionals: List[PyObjectId] = []
    
    # Status
    status: str = "pending"  # "pending", "in_progress", "completed", "certified"
    
    # Datas
    start_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    completion_date: Optional[datetime] = None
    
    # Avaliações
    professional_rating: Optional[float] = None
    project_manager_rating: Optional[float] = None
    project_owner_rating: Optional[float] = None
    
    # Notas
    notes: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
