# Importa o módulo create_engine do SQLAlchemy, que cria a conexão com o banco
from sqlalchemy import create_engine

# Importa sessionmaker e declarative_base do SQLAlchemy
# sessionmaker → cria sessões para interagir com o banco
# declarative_base → base para criar os modelos (tabelas)
from sqlalchemy.orm import sessionmaker, declarative_base

# Define a URL do banco de dados
# sqlite:///./artworks.db → banco SQLite chamado artworks.db na mesma pasta do projeto
SQLALCHEMY_DATABASE_URL = "sqlite:///./obras.db"

# Cria o engine de conexão com o banco
# connect_args={"check_same_thread": False} é necessário apenas para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma "fábrica" de sessões
# Cada vez que quisermos interagir com o banco, usamos SessionLocal()
SessionLocal = sessionmaker(
    autocommit=False,   # garante que alterações só acontecem após commit()
    autoflush=False,    # evita alterações salvas no automático (melhor controlar manualmente)
    bind=engine         # conecta ao engine criado acima
)

# Cria a classe base para os modelos (tabelas)
# Todos os modelos do projeto vão herdar dessa Base
Base = declarative_base()


'''

create_engine → conecta o Python ao banco.

sessionmaker → cria sessões que usamos para ler/escrever dados.

declarative_base → permite criar classes que se transformam em tabelas.

SQLALCHEMY_DATABASE_URL → indica onde o banco será armazenado.

SessionLocal → usamos ela para obter uma sessão sempre que precisarmos do banco.

---Sem flush, você só verá o id depois do commit.

Com flush, o SQLAlchemy já envia para o banco e consegue gerar o id, mas ainda é possível voltar atrás antes do commit.
'''
