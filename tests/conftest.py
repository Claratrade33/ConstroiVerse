# tests/conftest.py
import pytest
from backend.database import connect_to_mongodb, close_mongodb_connection

@pytest.fixture(scope="session", autouse=True)
def db_connection():
    # Configura a conexão com o banco de dados antes de todos os testes
    db = connect_to_mongodb()
    yield db
    # Fecha a conexão após todos os testes
    close_mongodb_connection()
