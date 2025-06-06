import pytest
from fastapi.testclient import TestClient
from api import app
from database import get_db, SessionLocal
from models import Account

client = TestClient(app)

@pytest.fixture
def test_db():
    """Cria uma instância temporária do banco de dados para testes."""
    db = SessionLocal()
    yield db
    db.close()

# 🏆 Testes para PUT /accounts
def test_create_account_success(test_db):
    """Testa a criação de uma conta nova."""
    response = client.put("/accounts", json={"id": 1, "name": "John Doe", "email": "johndoe@example.com"})
    assert response.status_code in [200, 201, 409]  # Inclui 409 se o ID já existir

    if response.status_code == 409:
        assert "detail" in response.json()
        assert response.json()["detail"] in ["Account with this ID already exists", "Account ID already exists"]
    else:
        assert response.json()["name"] == "John Doe"
        assert response.json()["email"] == "johndoe@example.com"

def test_create_account_conflict(test_db):
    """Testa a tentativa de criar uma conta com um ID já existente."""
    client.put("/accounts", json={"id": 1, "name": "John Doe", "email": "johndoe@example.com"})  # Criar conta inicial
    response = client.put("/accounts", json={"id": 1, "name": "Jane Doe", "email": "janedoe@example.com"})  # Tentar criar duplicado
    assert response.status_code == 409  # Deve retornar erro de conflito
    assert response.json()["detail"] in ["Account with this ID already exists", "Account ID already exists"]

# 🏆 Testes para GET /accounts
#def test_get_accounts_empty():
#    """Testa a listagem de contas quando o banco está vazio."""
#    response = client.get("/accounts")
#    assert response.status_code == 204  # Deve retornar No Content se não houver contas

def test_get_accounts_list(test_db):
    """Testa a listagem de contas quando há registros."""
    client.put("/accounts", json={"id": 2, "name": "Alice Doe", "email": "alice@example.com"})
    response = client.get("/accounts")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0  # Deve retornar contas

# 🏆 Testes para GET /accounts/{id}
def test_get_account_not_found():
    """Testa a busca por uma conta que não existe."""
    response = client.get("/accounts/999")  # ID que não existe
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"

def test_get_account_success(test_db):
    """Testa a busca de uma conta específica."""
    client.put("/accounts", json={"id": 3, "name": "Bob Doe", "email": "bob@example.com"})
    response = client.get("/accounts/3")

    assert response.status_code == 200
    assert response.json()["name"] == "Bob Doe"
    assert response.json()["email"] == "bob@example.com"

# 🏆 Testes para DELETE /accounts/{id}
def test_delete_account_not_found():
    """Testa a exclusão de uma conta inexistente."""
    response = client.delete("/accounts/999")  # Tentando excluir uma conta que não existe
    assert response.status_code == 404
    assert response.json()["detail"] == "Account not found"

def test_delete_account_success(test_db):
    """Testa a exclusão de uma conta existente."""
    client.put("/accounts", json={"id": 4, "name": "Charlie Doe", "email": "charlie@example.com"})  # Criar conta
    response = client.delete("/accounts/4")  # Deletar conta
    assert response.status_code == 200
    assert response.json()["message"] == "Account successfully deleted"

    # Verificar se a conta foi realmente removida
    response = client.get("/accounts/4")
    assert response.status_code == 404
