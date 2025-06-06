from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
from typing import Generator
import os

DATABASE_URL = os.getenv('DATABASE_URL',"postgresql://postgres:minhasenha@localhost:5432/ningipoints")

# Criando a engine com suporte a futuras versões
engine = create_engine(DATABASE_URL, future=True)

# Configuração do sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criando as tabelas automaticamente ao inicializar o banco
Base.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    """Gera uma sessão do banco de dados para uso em dependências do FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
