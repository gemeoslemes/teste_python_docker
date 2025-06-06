from fastapi import FastAPI, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from models import Account, Operation, OperationType
from database import get_db
from schemas import AccountCreate, OperationCreate
from typing import List

app = FastAPI()

# Manutenção dos endpoints existentes
@app.put("/accounts", status_code=201)
def create_account(account: AccountCreate, db: Session = Depends(get_db)) -> dict:
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
        raise HTTPException(status_code=204, detail="No accounts found")

    # ✅ Correção: Convertendo objetos SQLAlchemy para Pydantic
    return [AccountCreate(id=acc.id, name=acc.name, email=acc.email) for acc in accounts]

@app.get("/accounts/{account_id}", response_model=AccountCreate)
def get_account(account_id: int, db: Session = Depends(get_db)) -> AccountCreate:
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return AccountCreate(id=account.id, name=account.name, email=account.email)

@app.delete("/accounts/{account_id}", status_code=204)
def delete_account(account_id: int, response: Response, db: Session = Depends(get_db)) -> None:
    """Remove uma conta do banco de dados e todas suas operações."""
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # ✅ Exclui todas as operações relacionadas antes de remover a conta
    db.query(Operation).filter(Operation.account_id == account_id).delete()

    db.delete(account)
    db.commit()

    response.status_code = 204  # ✅ Define explicitamente o status 204
    return None  # ✅ Retorna None para evitar resposta JSON

# 🆕 Adição dos novos endpoints
@app.post("/accounts/{account_id}/operations", status_code=201)
def create_operation(account_id: int, operation: OperationCreate, db: Session = Depends(get_db)) -> dict:
    """Adiciona uma operação a uma conta existente."""
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    new_operation = Operation(
        account_id=account_id,
        operation=operation.operation,
        amount=operation.amount
    )
    db.add(new_operation)
    db.commit()
    db.refresh(new_operation)

    return {"message": "Operation successfully added", "operation_id": new_operation.id}

@app.get("/accounts/{account_id}/operations", response_model=list[OperationCreate])
def get_operations(account_id: int, db: Session = Depends(get_db)) -> list[OperationCreate]:
    """Retorna todas as operações de uma conta existente."""
    operations = db.query(Operation).filter(Operation.account_id == account_id).all()

    if not operations:
        raise HTTPException(status_code=204, detail="No operations found")

    # ✅ Correção: Convertendo objetos SQLAlchemy para Pydantic
    return [OperationCreate(operation=op.operation, amount=op.amount) for op in operations]
