import pytest
from flask import Flask
from backend.database import get_db
from backend.models.mongodb_models import Usuario
from bson import ObjectId

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
    db.usuarios.delete_many({})
    yield
    db.usuarios.delete_many({})

def test_create_user(client):
    response = client.post(
        '/users',
        json={
            "nome": "Teste User",
            "email": "teste@example.com",
            "senha": "password123",
            "tipo_usuario": "cliente"
        }
    )
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["nome"] == "Teste User"

def test_get_users(client):
    # Criar um usuário para listar
    client.post(
        '/users',
        json={
            "nome": "Teste User 1",
            "email": "teste1@example.com",
            "senha": "password123",
            "tipo_usuario": "cliente"
        }
    )
    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["nome"] == "Teste User 1"

def test_get_user_by_id(client):
    # Criar um usuário para buscar
    create_response = client.post(
        '/users',
        json={
            "nome": "Teste User 2",
            "email": "teste2@example.com",
            "senha": "password123",
            "tipo_usuario": "profissional"
        }
    )
    user_id = create_response.json["id"]
    
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json["nome"] == "Teste User 2"

def test_update_user(client):
    # Criar um usuário para atualizar
    create_response = client.post(
        '/users',
        json={
            "nome": "Teste User 3",
            "email": "teste3@example.com",
            "senha": "password123",
            "tipo_usuario": "cliente"
        }
    )
    user_id = create_response.json["id"]
    
    update_response = client.put(
        f'/users/{user_id}',
        json={
            "nome": "Teste User 3 Updated",
            "email": "teste3_updated@example.com"
        }
    )
    assert update_response.status_code == 200
    assert update_response.json["nome"] == "Teste User 3 Updated"

def test_delete_user(client):
    # Criar um usuário para deletar
    create_response = client.post(
        '/users',
        json={
            "nome": "Teste User 4",
            "email": "teste4@example.com",
            "senha": "password123",
            "tipo_usuario": "profissional"
        }
    )
    user_id = create_response.json["id"]
    
    delete_response = client.delete(f'/users/{user_id}')
    assert delete_response.status_code == 200
    assert delete_response.json["mensagem"] == "Usuário deletado com sucesso"
    
    get_response = client.get(f'/users/{user_id}')
    assert get_response.status_code == 404

