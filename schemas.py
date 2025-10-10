from pydantic import BaseModel
from typing import Optional

from pydantic import BaseModel

# Schema para criar uma obra
class ObraCreate(BaseModel):
    nome: str            # Nome da obra (obrigatório)
    colecao: str         # Nome da coleção (obrigatório)
    ano: int             # Ano da criação (obrigatório)
    categoria: str       # Categoria da obra (obrigatório)
    imagem_url: str      # Caminho ou URL da imagem (obrigatório)

# Schema para retornar uma obra
class ObraRead(BaseModel):
    id: int
    nome: str
    colecao: str
    ano: int
    categoria: str
    arquivado: bool
    imagem_url: str

    class Config:
        orm_mode = True
