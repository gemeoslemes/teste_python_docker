from pydantic import BaseModel, EmailStr

class AccountCreate(BaseModel):
    id: int
    name: str
    email: str