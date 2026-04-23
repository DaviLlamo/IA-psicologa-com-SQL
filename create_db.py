from database import engine, Base
import models

print("Criando banco de dados...")

Base.metadata.create_all(bind=engine)

print("Banco criado com sucesso!")