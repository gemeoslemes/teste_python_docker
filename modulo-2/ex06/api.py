from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, EmailStr
from decimal import Decimal
import json
from typing import Any

app: FastAPI = FastAPI()

class Account(BaseModel):
    name: str
    age: int
    email: EmailStr
    balance: Decimal

def read_json(filename: str) -> str:
    """Lê um arquivo JSON e retorna seu conteúdo."""
    try:
        with open(filename, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permissão negada para ler o arquivo.")
    except IsADirectoryError:
        raise HTTPException(status_code=400, detail="O argumento enviado é um diretório.")
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {erro.__class__.__name__}")

def obter_extensao(filename: str) -> str:
    """Verifica se a extensão do arquivo é JSON."""
    extensao: str = filename.split('.')[-1]
    if extensao != "json":
        raise ValueError("Extensão inválida")
    return extensao

@app.post("/create", status_code=201)
async def create_account(account: Account) -> dict[str, Any]:
    """Cria uma conta se os dados forem válidos."""
    try:
        return {"message": "Conta criada com sucesso!", "account": account.model_dump()}
    except ValidationError as error:
        raise HTTPException(status_code=422, detail=f"Erro na validação dos campos: {error}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)