from pydantic import BaseModel
from models import OperationType

class AccountCreate(BaseModel):
    id: int
    name: str
    email: str

class OperationCreate(BaseModel):
    operation: OperationType  # Débito ou crédito
    amount: int
