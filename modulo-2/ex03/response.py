import sys
import httpx
from typing import NoReturn

def fetch_url(url: str) -> None:
    try:
        response: httpx.Response = httpx.get(url)
        print(f"{response.status_code} {response.reason_phrase}")
    except httpx.ConnectError as e:
        print("Error: ConnectError")
        raise e  # Mantém a exceção para que pytest capture
    except httpx.RequestError as e:
        print("Error: RequestError")
        raise e

def main() -> NoReturn:
    if len(sys.argv) != 2:
        print("Uso: python3 response.py <URL>")
        sys.exit(1)  # Encerra o programa corretamente

    url: str = sys.argv[1]
    try:
        fetch_url(url)
    except httpx.ConnectError:
        sys.exit(1)  # Encerra com erro

    sys.exit(0)  # Adiciona um encerramento explícito para evitar erro no mypy

if __name__ == "__main__":
    main()