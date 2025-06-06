import requests
from typing import Tuple, Dict, Any

URL = "https://jsonplaceholder.typicode.com/posts"

def do_GET() -> Tuple[int, Dict[str, Any]]:
    response = requests.get(URL + "/1")  # Obtendo o primeiro post
    return response.status_code, response.json()

def do_POST() -> Tuple[int, Dict[str, Any]]:
    data = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    response = requests.post(URL, json=data)  # Agora a URL está correta
    return response.status_code, response.json()

def main() -> None:
    print(*do_GET())
    print(*do_POST())

if __name__ == "__main__":
    main()