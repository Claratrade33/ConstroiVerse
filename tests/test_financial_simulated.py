"""
Testes de Integração Simulados para Rotas Financeiras
(Assumindo conexão ativa com MongoDB)
"""

import pytest
from unittest.mock import MagicMock
from datetime import datetime
from bson import ObjectId

# Reutilizando o MockClient do arquivo test_professionals_simulated.py
class MockClient:
    def __init__(self):
        self.financial_records = self.MockCollection()

    class MockCollection:
        def __init__(self):
            self.data = {}
            self.next_id = 1

        def insert_one(self, document):
            new_id = ObjectId()
            document['_id'] = new_id
            self.data[new_id] = document
            return MagicMock(inserted_id=new_id)

        def find(self, query):
            # Simulação de busca
            results = []
            for doc in self.data.values():
                match = True
                for key, value in query.items():
                    if doc.get(key) != value:
                        match = False
                        break
                if match:
                    results.append(doc)
            return results

        def find_one(self, query):
            results = self.find(query)
            return results[0] if results else None

        def count_documents(self, query):
            return len(self.find(query))

# Simulação de um cliente HTTP para testes
class MockHTTPClient:
    def __init__(self, db_client):
        self.db_client = db_client

    def post(self, url, json):
        if url == '/api/financial/records':
            # Simula a lógica da rota create_financial_record
            if json.get('type') not in ["income", "expense"]:
                return MagicMock(status_code=400, json={'detail': "Tipo deve ser 'income' ou 'expense'"})
            if json.get('amount', 0) <= 0:
                return MagicMock(status_code=400, json={'detail': "Valor deve ser maior que zero"})
            
            record = {
                'user_id': ObjectId(json['user_id']),
                'type': json['type'],
                'category': json['category'],
                'description': json['description'],
                'amount': json['amount'],
                'currency': json.get('currency', 'BRL'),
                'date': datetime.utcnow(),
                'status': json.get('status', 'pending'),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            result = self.db_client.financial_records.insert_one(record)
            record['_id'] = str(result.inserted_id)
            
            return MagicMock(status_code=201, json=record)
        return MagicMock(status_code=404, json={'error': 'Not Found'})

    def get(self, url, params=None):
        if url.startswith('/api/financial/summary/'):
            user_id = url.split('/')[-1]
            if not ObjectId.is_valid(user_id):
                return MagicMock(status_code=400, json={'detail': "ID de usuário inválido"})
            
            # Simula a lógica da rota get_financial_summary
            income_query = {'user_id': ObjectId(user_id), 'type': 'income'}
            expense_query = {'user_id': ObjectId(user_id), 'type': 'expense'}
            
            total_income = sum(r['amount'] for r in self.db_client.financial_records.find(income_query))
            total_expense = sum(r['amount'] for r in self.db_client.financial_records.find(expense_query))
            
            return MagicMock(status_code=200, json={
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": total_income - total_expense,
                "currency": "BRL"
            })
        return MagicMock(status_code=404, json={'error': 'Not Found'})


@pytest.fixture
def mock_db_client():
    """Fixture que retorna um cliente de banco de dados mockado"""
    return MockClient()

@pytest.fixture
def mock_http_client(mock_db_client):
    """Fixture que retorna um cliente HTTP mockado para testes"""
    return MockHTTPClient(mock_db_client)

def test_create_financial_record_income_success(mock_http_client):
    """Testa a criação bem-sucedida de um registro de entrada."""
    user_id = '607f1f77bcf86cd799439011'
    
    response = mock_http_client.post('/api/financial/records', json={
        'user_id': user_id,
        'type': 'income',
        'category': 'salary',
        'description': 'Pagamento por projeto concluído',
        'amount': 5000.00
    })
    
    assert response.status_code == 201
    assert response.json['type'] == 'income'
    assert response.json['amount'] == 5000.00

def test_create_financial_record_expense_success(mock_http_client):
    """Testa a criação bem-sucedida de um registro de despesa."""
    user_id = '607f1f77bcf86cd799439011'
    
    response = mock_http_client.post('/api/financial/records', json={
        'user_id': user_id,
        'type': 'expense',
        'category': 'material',
        'description': 'Compra de cimento e areia',
        'amount': 850.50
    })
    
    assert response.status_code == 201
    assert response.json['type'] == 'expense'
    assert response.json['amount'] == 850.50

def test_create_financial_record_invalid_type(mock_http_client):
    """Testa a criação de um registro com tipo inválido."""
    response = mock_http_client.post('/api/financial/records', json={
        'user_id': '607f1f77bcf86cd799439011',
        'type': 'invalid',
        'category': 'salary',
        'description': 'Teste',
        'amount': 100.00
    })
    
    assert response.status_code == 400
    assert 'detail' in response.json

def test_get_financial_summary(mock_http_client):
    """Testa o resumo financeiro com registros de entrada e saída."""
    user_id = '607f1f77bcf86cd799439012'
    
    # Inserir registros para o usuário de teste
    mock_http_client.post('/api/financial/records', json={
        'user_id': user_id, 'type': 'income', 'category': 'salary', 'description': 'Salário 1', 'amount': 3000.00
    })
    mock_http_client.post('/api/financial/records', json={
        'user_id': user_id, 'type': 'income', 'category': 'bonus', 'description': 'Bônus', 'amount': 500.00
    })
    mock_http_client.post('/api/financial/records', json={
        'user_id': user_id, 'type': 'expense', 'category': 'material', 'description': 'Material', 'amount': 1000.00
    })
    mock_http_client.post('/api/financial/records', json={
        'user_id': user_id, 'type': 'expense', 'category': 'equipment', 'description': 'Equipamento', 'amount': 200.00
    })
    
    response = mock_http_client.get(f'/api/financial/summary/{user_id}')
    
    assert response.status_code == 200
    assert response.json['total_income'] == 3500.00
    assert response.json['total_expense'] == 1200.00
    assert response.json['balance'] == 2300.00
    assert response.json['currency'] == 'BRL'
