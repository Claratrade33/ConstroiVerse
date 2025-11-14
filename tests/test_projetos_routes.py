import pytest
from backend.database import get_db
from backend.models.mongodb_models import Projeto, PerfilProfissional, Usuario
from bson import ObjectId
from datetime import datetime

# Configuração do aplicativo Flask para testes
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    # Adicione aqui as configurações necessárias para o ambiente de teste, se houver
    # Por exemplo, uma URI de banco de dados de teste
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clean_db():
    # Limpa o banco de dados de teste antes de cada teste
    db = get_db()
    db.projetos.delete_many({})
    db.usuarios.delete_many({})
    db.perfis_profissionais.delete_many({})
    yield
    db.projetos.delete_many({})
    db.usuarios.delete_many({})
    db.perfis_profissionais.delete_many({})

@pytest.fixture
def setup_data():
    db = get_db()
    # Criar um usuário cliente
    cliente_data = {
        "nome": "Cliente Teste",
        "email": "cliente@example.com",
        "senha": "senha123",
        "tipo_usuario": "cliente",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    cliente_id = str(db.usuarios.insert_one(cliente_data).inserted_id)

    # Criar um usuário profissional
    profissional_user_data = {
        "nome": "Profissional Teste",
        "email": "profissional@example.com",
        "senha": "senha123",
        "tipo_usuario": "profissional",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    profissional_user_id = str(db.usuarios.insert_one(profissional_user_data).inserted_id)

    # Criar um perfil profissional
    profissional_perfil_data = {
        "usuario_id": profissional_user_id,
        "profissao": "Arquiteto",
        "crea_cau": "123456",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    profissional_perfil_id = str(db.perfis_profissionais.insert_one(profissional_perfil_data).inserted_id)

    return {
        "cliente_id": cliente_id,
        "profissional_user_id": profissional_user_id,
        "profissional_perfil_id": profissional_perfil_id
    }

def test_create_projeto(client, setup_data):
    cliente_id = setup_data["cliente_id"]
    profissional_user_id = setup_data["profissional_user_id"]

    response = client.post(
        '/projetos',
        json={
            "nome_projeto": "Projeto Teste",
            "descricao": "Descrição do projeto de teste",
            "profissional_id": profissional_user_id,
            "cliente_id": cliente_id,
            "tipo_projeto": "residencial",
            "area_construida": 100.0,
            "orcamento_estimado": 50000.0,
            "status": "planejamento",
            "data_inicio": datetime.utcnow().isoformat(),
            "data_fim_prevista": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
    )
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["nome_projeto"] == "Projeto Teste"

def test_list_projetos(client, setup_data):
    cliente_id = setup_data["cliente_id"]
    profissional_user_id = setup_data["profissional_user_id"]

    # Criar um projeto para listar
    client.post(
        '/projetos',
        json={
            "nome_projeto": "Projeto Teste 1",
            "descricao": "Descrição do projeto de teste 1",
            "profissional_id": profissional_user_id,
            "cliente_id": cliente_id,
            "tipo_projeto": "comercial",
            "area_construida": 200.0,
            "orcamento_estimado": 100000.0,
            "status": "em_andamento",
            "data_inicio": datetime.utcnow().isoformat(),
            "data_fim_prevista": (datetime.utcnow() + timedelta(days=60)).isoformat()
        }
    )
    response = client.get('/projetos')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["nome_projeto"] == "Projeto Teste 1"

def test_get_projeto_by_id(client, setup_data):
    cliente_id = setup_data["cliente_id"]
    profissional_user_id = setup_data["profissional_user_id"]

    # Criar um projeto para buscar
    create_response = client.post(
        '/projetos',
        json={
            "nome_projeto": "Projeto Teste 2",
            "descricao": "Descrição do projeto de teste 2",
            "profissional_id": profissional_user_id,
            "cliente_id": cliente_id,
            "tipo_projeto": "residencial",
            "area_construida": 150.0,
            "orcamento_estimado": 75000.0,
            "status": "concluido",
            "data_inicio": datetime.utcnow().isoformat(),
            "data_fim_prevista": (datetime.utcnow() + timedelta(days=90)).isoformat()
        }
    )
    projeto_id = create_response.json["id"]
    
    response = client.get(f'/projetos/{projeto_id}')
    assert response.status_code == 200
    assert response.json["nome_projeto"] == "Projeto Teste 2"

def test_update_projeto(client, setup_data):
    cliente_id = setup_data["cliente_id"]
    profissional_user_id = setup_data["profissional_user_id"]

    # Criar um projeto para atualizar
    create_response = client.post(
        '/projetos',
        json={
            "nome_projeto": "Projeto Teste 3",
            "descricao": "Descrição do projeto de teste 3",
            "profissional_id": profissional_user_id,
            "cliente_id": cliente_id,
            "tipo_projeto": "residencial",
            "area_construida": 120.0,
            "orcamento_estimado": 60000.0,
            "status": "planejamento",
            "data_inicio": datetime.utcnow().isoformat(),
            "data_fim_prevista": (datetime.utcnow() + timedelta(days=45)).isoformat()
        }
    )
    projeto_id = create_response.json["id"]
    
    update_response = client.put(
        f'/projetos/{projeto_id}',
        json={
            "nome_projeto": "Projeto Teste 3 Atualizado",
            "status": "em_andamento"
        }
    )
    assert update_response.status_code == 200
    assert update_response.json["nome_projeto"] == "Projeto Teste 3 Atualizado"
    assert update_response.json["status"] == "em_andamento"

def test_delete_projeto(client, setup_data):
    cliente_id = setup_data["cliente_id"]
    profissional_user_id = setup_data["profissional_user_id"]

    # Criar um projeto para deletar
    create_response = client.post(
        '/projetos',
        json={
            "nome_projeto": "Projeto Teste 4",
            "descricao": "Descrição do projeto de teste 4",
            "profissional_id": profissional_user_id,
            "cliente_id": cliente_id,
            "tipo_projeto": "comercial",
            "area_construida": 80.0,
            "orcamento_estimado": 40000.0,
            "status": "cancelado",
            "data_inicio": datetime.utcnow().isoformat(),
            "data_fim_prevista": (datetime.utcnow() + timedelta(days=15)).isoformat()
        }
    )
    projeto_id = create_response.json["id"]
    
    delete_response = client.delete(f'/projetos/{projeto_id}')
    assert delete_response.status_code == 200
    assert delete_response.json["mensagem"] == "Projeto deletado com sucesso"
    
    get_response = client.get(f'/projetos/{projeto_id}')
    assert get_response.status_code == 404

