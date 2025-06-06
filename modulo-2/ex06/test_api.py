from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_create_account_success():
    """Teste para criar uma conta com dados válidos."""
    response = client.post("/create", json={
        "name": "Charles",
        "age": 30,
        "email": "charles@example.com",
        "balance": 1500.75
    })
    assert response.status_code == 201
    assert response.json()["message"] == "Conta criada com sucesso!"

def test_create_account_failure():
    """Teste para criar uma conta com dados inválidos."""
    response = client.post("/create", json={
        "name": "Charles",
        "age": "trinta",  # Deve ser um número inteiro
        "email": "charles.com",  # E-mail inválido
        "balance": "NaN"  # Valor não numérico
    })
    assert response.status_code == 422

def test_create_account_missing_field():
    """Teste para criar uma conta sem um campo obrigatório."""
    response = client.post("/create", json={
        "name": "Charles",
        "email": "charles@example.com"
        # Faltando 'age' e 'balance'
    })
    assert response.status_code == 422