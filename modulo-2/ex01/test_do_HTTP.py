import pytest
import requests_mock
from do_HTTP import do_GET, do_POST

URL = "https://jsonplaceholder.typicode.com/posts"

def test_do_GET():
    with requests_mock.Mocker() as mocker:
        mocker.get(URL + "/1", json={"userId": 1, "id": 1, "title": "foo", "body": "bar"}, status_code=200)
        status_code, response_json = do_GET()
        
        assert status_code == 200
        assert response_json["id"] == 1
        assert response_json["title"] == "foo"
        assert response_json["body"] == "bar"

def test_do_POST():
    with requests_mock.Mocker() as mocker:
        mocker.post(URL, json={"title": "foo", "body": "bar", "userId": 1, "id": 101}, status_code=201)
        status_code, response_json = do_POST()
        
        assert status_code == 201
        assert response_json["id"] == 101
        assert response_json["title"] == "foo"
        assert response_json["body"] == "bar"