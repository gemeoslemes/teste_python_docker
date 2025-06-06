import os
from sqlalchemy import create_engine
from models import Base

# Pegando variáveis de ambiente
DATABASE_URL = f"postgresql://postgres:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/ningipoints"

# Criando a conexão com o banco
engine = create_engine(DATABASE_URL)

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)

print("Tabelas criadas com sucesso!")