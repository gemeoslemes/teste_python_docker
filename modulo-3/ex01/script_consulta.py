from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Consultando todas as contas
accounts = session.query(Account).all()
for account in accounts:
    print(f"ID: {account.id}, Nome: {account.name}, Email: {account.email}")

# Fechando a sessão
session.close()