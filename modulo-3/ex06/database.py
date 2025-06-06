import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
from typing import Generator

# Ajustando para se conectar ao banco dentro do contêiner
DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://postgres:minhasenha@postgres_db:5432/ningipoints")

# Criando a engine
engine = create_engine(DATABASE_URL, future=True)

# Criando a sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar tabelas automaticamente
Base.metadata.create_all(engine)

def get_db() -> Generator[Session, None, None]:
    """Gera uma sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
