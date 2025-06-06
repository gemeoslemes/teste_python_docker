import pytest
import httpx
import requests_mock
from response import fetch_url

URL_VALID = "https://www.google.com"
URL_NOT_FOUND = "https://42.fr/unknown"
URL_INVALID = "https://invalidaddress"

def test_fetch_url_valid():
    with requests_mock.Mocker() as mocker:
        mocker.get(URL_VALID, status_code=200, reason="OK")
        fetch_url(URL_VALID)  # Esperado: "200 OK"

def test_fetch_url_not_found():
    with requests_mock.Mocker() as mocker:
        mocker.get(URL_NOT_FOUND, status_code=404, reason="Not Found")
        fetch_url(URL_NOT_FOUND)  # Esperado: "404 Not Found"

def test_fetch_url_connect_error():
    with pytest.raises(httpx.ConnectError):  # Agora a exceção será corretamente levantada
        fetch_url(URL_INVALID)