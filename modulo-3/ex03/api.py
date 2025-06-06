from typing import List
from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from models import Account
from database import get_db
from schemas import AccountCreate

app = FastAPI()

@app.put("/accounts", status_code=201)
def create_account(account: AccountCreate, db: Session = Depends(get_db)) -> dict:
    """Cria uma nova conta se o ID não existir no banco de dados."""
    existing_account = db.query(Account).filter(Account.id == account.id).first()
    if existing_account:
        raise HTTPException(status_code=409, detail="Account ID already exists")

    new_account = Account(id=account.id, name=account.name, email=account.email)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return {
        "message": "Account successfully created",
        "name": new_account.name,
        "email": new_account.email
    }

@app.get("/accounts", response_model=list[AccountCreate])
def get_accounts(db: Session = Depends(get_db)) -> list[AccountCreate]:
    """Retorna todas as contas registradas no banco de dados."""
    accounts = db.query(Account).all()
    
    if not accounts:
        raise HTTPException(status_code=204, detail="No accounts found")  # Retorna 204 se não houver contas
    
    return accounts


@app.get("/accounts/{account_id}", response_model=AccountCreate)
def get_account(account_id: int, db: Session = Depends(get_db)) -> AccountCreate:
    """Retorna os dados de uma conta específica e suas operações."""
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")  # Retorna 404 se a conta não existir
    
    return AccountCreate(id=account.id, name=account.name, email=account.email)

@app.delete("/accounts/{account_id}", status_code=200)
def delete_account(account_id: int, db: Session = Depends(get_db)) -> dict:
    """Remove uma conta do banco de dados."""
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")  # Retorna erro se a conta não existir

    db.delete(account)
    db.commit()  # ✅ Aqui está correto

    return {"message": "Account successfully deleted"}
