from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Account
from database import get_db
from schemas import AccountCreate

app = FastAPI()

@app.put("/accounts", status_code=201)
def create_account(account: AccountCreate, db: Session = Depends(get_db)) -> dict:
    """Cria uma nova conta se o ID não existir no banco de dados."""
    
    # Verifica se a conta já existe
    existing_account = db.query(Account).filter(Account.id == account.id).first()
    if existing_account:
        raise HTTPException(status_code=409, detail="Account ID already exists")

    # Cria um novo registro no banco de dados
    new_account = Account(id=account.id, name=account.name, email=account.email)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {
        "message": "Account successfully created",
        "name": new_account.name,
        "email": new_account.email
    }
