# Guia de Desenvolvimento - Construiverse

## Introdução

Este guia fornece instruções detalhadas para continuar o desenvolvimento do Construiverse, implementando as funcionalidades restantes e integrando o MongoDB Atlas.

## Pré-requisitos

- Python 3.8+
- MongoDB Atlas (conta criada)
- Git
- Node.js (para frontend)
- Conhecimento básico de Flask, MongoDB e React

## Configuração do Ambiente

### 1. Clonar o Repositório

```bash
gh repo clone Construiverse/ConstroiVerse /home/ubuntu/construiverse-unified
cd /home/ubuntu/construiverse-unified
```

### 2. Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto backend:

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://fragmentosdaalma33_db_user:<password>@cluster0.dxbozq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0

# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=construiverse#2025$SECRET

# JWT
JWT_SECRET_KEY=seu_jwt_secret_key_aqui
JWT_ALGORITHM=HS256

# AWS (para deploy)
AWS_ACCESS_KEY_ID=sua_chave_aqui
AWS_SECRET_ACCESS_KEY=sua_chave_secreta_aqui
AWS_REGION=sa-east-1
```

### 4. Iniciar o Servidor

```bash
python src/main.py
```

O servidor estará disponível em `http://localhost:5000`

## Implementação de Funcionalidades

### Fase 1: Autenticação e Autorização

#### Objetivo
Implementar sistema seguro de autenticação com JWT.

#### Arquivos a Modificar
- `backend/src/routes/auth.py` (criar novo)
- `backend/src/utils/jwt_handler.py` (criar novo)
- `backend/src/middleware/auth_middleware.py` (criar novo)

#### Passos
1. Criar rotas de registro e login
2. Implementar hashing de senhas com bcrypt
3. Gerar e validar tokens JWT
4. Criar middleware de autenticação
5. Proteger rotas com autenticação

#### Exemplo de Implementação

```python
# backend/src/routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validações
    if not data.get('email') or not data.get('senha'):
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    # Verificar se usuário já existe
    # db.usuarios.find_one({'email': data['email']})
    
    # Criar novo usuário
    usuario = {
        'nome': data.get('nome'),
        'email': data['email'],
        'senha_hash': generate_password_hash(data['senha']),
        'tipo_usuario': data.get('tipo_usuario', 'Cliente'),
        'data_criacao': datetime.utcnow(),
        'ativo': True
    }
    
    # db.usuarios.insert_one(usuario)
    
    return jsonify({'message': 'Usuário registrado com sucesso'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validações
    if not data.get('email') or not data.get('senha'):
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400
    
    # Buscar usuário
    # usuario = db.usuarios.find_one({'email': data['email']})
    
    # Verificar senha
    # if not check_password_hash(usuario['senha_hash'], data['senha']):
    #     return jsonify({'error': 'Email ou senha incorretos'}), 401
    
    # Gerar token JWT
    token = jwt.encode({
        'user_id': str(usuario['_id']),
        'email': usuario['email'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
    
    return jsonify({'token': token}), 200
```

### Fase 2: Integração Completa com MongoDB

#### Objetivo
Conectar todas as rotas ao MongoDB Atlas.

#### Arquivos a Modificar
- `backend/src/config/database.py`
- `backend/src/routes/*.py` (todas as rotas)

#### Passos
1. Configurar conexão com MongoDB Atlas
2. Implementar CRUD operations para cada modelo
3. Adicionar validações de entrada
4. Implementar tratamento de erros
5. Adicionar índices para otimização

#### Exemplo de Implementação

```python
# backend/src/config/database.py
from pymongo import MongoClient
import os

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
    
    def connect(self):
        uri = os.getenv('MONGODB_URI')
        self.client = MongoClient(uri)
        self.db = self.client['construiverse']
        print("Conectado ao MongoDB Atlas")
    
    def disconnect(self):
        if self.client:
            self.client.close()
    
    def get_db(self):
        return self.db

mongodb = MongoDB()
```

### Fase 3: Implementar Rotas com MongoDB

#### Objetivo
Completar a implementação de todas as rotas com operações no MongoDB.

#### Exemplo para Profissionais

```python
# backend/src/routes/professionals.py
from flask import Blueprint, request, jsonify
from bson import ObjectId
from datetime import datetime
from ..config.database import mongodb

professionals_bp = Blueprint('professionals', __name__)

@professionals_bp.route('/professionals', methods=['GET'])
def list_professionals():
    db = mongodb.get_db()
    
    # Filtros
    profession = request.args.get('profession')
    location = request.args.get('location')
    min_rating = request.args.get('min_rating', type=float)
    
    query = {}
    if profession:
        query['profession'] = profession
    if location:
        query['location'] = location
    if min_rating:
        query['average_rating'] = {'$gte': min_rating}
    
    professionals = list(db.professionals.find(query).limit(10))
    
    # Converter ObjectId para string
    for prof in professionals:
        prof['_id'] = str(prof['_id'])
    
    return jsonify(professionals), 200

@professionals_bp.route('/professionals', methods=['POST'])
def create_professional():
    db = mongodb.get_db()
    data = request.get_json()
    
    # Validações
    required_fields = ['user_id', 'name', 'email', 'phone', 'profession']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Campos obrigatórios faltando'}), 400
    
    professional = {
        'user_id': ObjectId(data['user_id']),
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'profession': data['profession'],
        'location': data.get('location'),
        'experience_years': data.get('experience_years', 0),
        'average_rating': 0.0,
        'total_reviews': 0,
        'reviews': [],
        'is_available': True,
        'specialties': data.get('specialties', []),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    
    result = db.professionals.insert_one(professional)
    professional['_id'] = str(result.inserted_id)
    
    return jsonify(professional), 201
```

### Fase 4: Testes de Integração

#### Objetivo
Criar testes para validar funcionalidades.

#### Exemplo de Teste

```python
# tests/test_professionals.py
import pytest
from datetime import datetime

def test_create_professional(client):
    response = client.post('/api/professionals', json={
        'user_id': '507f1f77bcf86cd799439011',
        'name': 'João Silva',
        'email': 'joao@example.com',
        'phone': '+55 11 98765-4321',
        'profession': 'Pedreiro',
        'location': 'São Paulo, SP',
        'experience_years': 10,
        'specialties': ['Fundação', 'Alvenaria']
    })
    
    assert response.status_code == 201
    assert response.json['name'] == 'João Silva'

def test_list_professionals(client):
    response = client.get('/api/professionals')
    assert response.status_code == 200
    assert isinstance(response.json, list)
```

### Fase 5: Frontend com React

#### Objetivo
Desenvolver interface de usuário moderna e responsiva.

#### Estrutura do Frontend

```
frontend/
├── src/
│   ├── components/
│   │   ├── ProfessionalCard.jsx
│   │   ├── ProjectForm.jsx
│   │   ├── FinancialDashboard.jsx
│   │   └── ChatWindow.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Professionals.jsx
│   │   ├── Projects.jsx
│   │   ├── Financial.jsx
│   │   └── RealEstate.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   └── main.jsx
├── package.json
└── vite.config.js
```

#### Exemplo de Componente

```jsx
// frontend/src/components/ProfessionalCard.jsx
import React from 'react';

export default function ProfessionalCard({ professional }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold">{professional.name}</h3>
      <p className="text-gray-600">{professional.profession}</p>
      <div className="flex items-center mt-2">
        <span className="text-yellow-500">★</span>
        <span className="ml-2">{professional.average_rating}/5</span>
        <span className="text-gray-500 ml-2">({professional.total_reviews} avaliações)</span>
      </div>
      <p className="text-gray-600 mt-2">{professional.location}</p>
      <button className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
        Contratar
      </button>
    </div>
  );
}
```

## Checklist de Implementação

### Backend
- [ ] Configurar MongoDB Atlas e variáveis de ambiente
- [ ] Implementar autenticação com JWT
- [ ] Completar CRUD para Profissionais
- [ ] Completar CRUD para Projetos
- [ ] Completar CRUD para Gestão Financeira
- [ ] Implementar Sistema de Comunicação
- [ ] Implementar Módulo Imobiliário
- [ ] Integrar SmartStore IA
- [ ] Adicionar testes de integração
- [ ] Documentar API com Swagger

### Frontend
- [ ] Configurar projeto React
- [ ] Criar layout principal
- [ ] Implementar página de Profissionais
- [ ] Implementar página de Projetos
- [ ] Implementar Dashboard Financeiro
- [ ] Implementar Sistema de Chat
- [ ] Implementar Módulo Imobiliário
- [ ] Adicionar autenticação
- [ ] Testes de componentes
- [ ] Deploy

### DevOps
- [ ] Configurar Docker
- [ ] Setup CI/CD com GitHub Actions
- [ ] Configurar AWS (EC2, RDS, S3)
- [ ] Setup de monitoramento
- [ ] Backup automático

## Boas Práticas

### Código
- Seguir PEP 8 para Python
- Usar type hints
- Documentar funções com docstrings
- Manter funções pequenas e focadas
- DRY (Don't Repeat Yourself)

### Banco de Dados
- Criar índices para campos frequentemente consultados
- Usar transações para operações críticas
- Implementar soft delete quando apropriado
- Manter histórico de alterações importantes

### API
- Usar status codes HTTP corretos
- Retornar mensagens de erro descritivas
- Implementar rate limiting
- Versionamento de API (v1, v2, etc)

### Segurança
- Validar todas as entradas
- Usar HTTPS em produção
- Implementar CORS corretamente
- Manter secrets em variáveis de ambiente
- Fazer backup regular

## Recursos Úteis

- [MongoDB Documentação](https://docs.mongodb.com/)
- [Flask Documentação](https://flask.palletsprojects.com/)
- [React Documentação](https://react.dev/)
- [JWT.io](https://jwt.io/)
- [AWS Documentação](https://docs.aws.amazon.com/)

## Suporte

Para dúvidas ou problemas, consulte:
1. A documentação do projeto
2. Os testes existentes
3. A comunidade do projeto

## Conclusão

Seguindo este guia, você terá uma base sólida para continuar o desenvolvimento do Construiverse. Lembre-se de testar frequentemente e manter a documentação atualizada.
