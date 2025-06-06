import pytest
import requests_mock
from format_json import fetch_project_data  # Importa a função do seu script

URL = "https://assets.breatheco.de/apis/fake/sample/project1.php"

def test_fetch_project_data():
    with requests_mock.Mocker() as mocker:
        mocker.get(URL, json={"name": "eLearning", "images": ["https://intra.42.fr?image=178"]}, status_code=200)

        project_name, first_image_url = fetch_project_data()

        assert project_name == "eLearning"
        assert first_image_url == "https://intra.42.fr?image=178"

def test_fetch_project_data_error():
    with requests_mock.Mocker() as mocker:
        mocker.get(URL, status_code=404)

        result = fetch_project_data()

        assert "Erro ao buscar dados" in result