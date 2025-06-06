from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bem-vindo à minha API!"}

def test_post_data_success():
    response = client.post("/", json={"name": "FastAPI"})
    assert response.status_code == 201

def test_post_data_failure():
    response = client.post("/", content="invalid data")
    assert response.status_code == 400

def test_get_info():
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert "now" in data
    assert "version" in data