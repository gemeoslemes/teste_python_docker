from fastapi import FastAPI, Request, HTTPException
import sys
from datetime import datetime
from typing import Dict, Any

app = FastAPI()

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Bem-vindo à minha API!"}

@app.post("/", status_code=201)
async def post_data(request: Request) -> Dict[str, str]:
    try:
        data: Dict[str, Any] = await request.json()
        if not data:
            raise HTTPException(status_code=400, detail="JSON inválido")
        return {"status": "success", "message": "Dados recebidos"}
    except Exception:
        raise HTTPException(status_code=400, detail="JSON inválido")

@app.get("/info")
async def get_info() -> Dict[str, str]:
    return {
        "now": datetime.utcnow().isoformat(),
        "version": sys.version
    }