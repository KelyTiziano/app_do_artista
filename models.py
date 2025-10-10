# Importamos os tipos de colunas que vamos usar no banco
# Cada tipo define que tipo de dado será armazenado (texto, número, etc)
from sqlalchemy import Column, Integer, String, Boolean

# Importamos o "Base" do arquivo database.py
# Todos os modelos (tabelas) herdam dessa Base
from database import Base

# Criamos a classe que representa a tabela de obras de arte
class Artwork(Base):
    # Nome da tabela no banco de dados
    __tablename__ = "obras"

    # Abaixo definimos as colunas da tabela
    # Cada atributo vira uma coluna no banco

    # ID único para cada obra
    # primary_key=True → identifica a linha de forma única
    # index=True → cria um índice para buscas mais rápidas
    id = Column(Integer, primary_key=True, index=True)

    # Nome da obra (obrigatório)
    # nullable=False → não pode ficar vazio
    nome = Column(String, nullable=False)

    # Nome da coleção (pode ser vazio)
    colecao = Column(String)

    # Ano de criação da obra (pode ser vazio)
    ano = Column(Integer)

    # Categoria da obra (por exemplo: "abstrato", "paisagem", etc)
    categoria = Column(String)

    # Define se a obra está arquivada (invisível para o público)
    # Por padrão, começa como False (visível)
    arquivado = Column(Boolean, default=False)

    # Caminho da imagem (URL ou nome do arquivo salvo)
    imagem_url = Column(String)


