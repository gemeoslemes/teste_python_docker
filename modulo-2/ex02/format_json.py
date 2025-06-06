import httpx
from typing import Tuple, Dict, Any, Union

# Simulação do endpoint (substitua pela URL real caso necessário)
URL = "https://assets.breatheco.de/apis/fake/sample/project1.php"

def fetch_project_data() -> Union[Tuple[str, str], str]:
    try:
        response = httpx.get(URL)
        response.raise_for_status()  # Levanta erro em caso de falha na requisição
        data: Dict[str, Any] = response.json()
        
        project_name: str = data["name"]
        first_image_url: str = data["images"][0]

        return project_name, first_image_url
    except Exception as e:
        return f"Erro ao buscar dados: {e}"

if __name__ == "__main__":
    result = fetch_project_data()
    print(result)