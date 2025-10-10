from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine
from schemas import ObraCreate, ObraRead  # Importa os schemas

# Cria as tabelas no banco, se ainda não existirem
# Essa linha garante que todas as tabelas definidas no models.py
# existam no banco de dados. Se não existirem, serão criadas.
models.Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI(title="API Artista Visual")

# DEPENDÊNCIA PARA O BANCO

def obter_sessao_db():
    """Cria uma sessão com o banco e garante que será fechada após uso"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROTA DE TESTE

@app.get("/")
def rota_principal():
    """Rota inicial de teste"""
    return {"mensagem": "🚀 API do artista visual está funcionando!"}

# LISTAR TODAS AS OBRAS

@app.get("/obras", response_model=list[ObraRead])
def listar_todas_obras(db: Session = Depends(obter_sessao_db)):
    """Retorna todas as obras cadastradas"""
    obras = db.query(models.Artwork).all()
    return obras

# LISTAR OBRAS VISÍVEIS AO PÚBLICO

@app.get("/obras/visiveis", response_model=list[ObraRead])
def listar_obras_visiveis(db: Session = Depends(obter_sessao_db)):
    """
    Retorna apenas as obras que NÃO estão arquivadas (arquivado = False),
    ou seja, visíveis ao público geral.
    """
    obras_visiveis = db.query(models.Artwork).filter(models.Artwork.arquivado == False).all()
    return obras_visiveis

# ADICIONAR UMA NOVA OBRA

@app.post("/obras", response_model=ObraRead)
def cadastrar_obra(obra: ObraCreate, db: Session = Depends(obter_sessao_db)):
    """
    Adiciona uma nova obra ao banco.
    Recebe um JSON com todos os campos obrigatórios:
    {
        "nome": "Nome da obra",
        "colecao": "Nome da coleção",
        "ano": 2025,
        "categoria": "Categoria",
        "imagem_url": "caminho/da/imagem"
    }
    """

    nova_obra = models.Artwork(
        nome=obra.nome,
        colecao=obra.colecao,
        ano=obra.ano,
        categoria=obra.categoria,
        imagem_url=obra.imagem_url
    )
    db.add(nova_obra)
    db.commit()
    db.refresh(nova_obra)  # pega o ID gerado
    return nova_obra

    # ARQUIVAR UMA OBRA
@app.put("/obras/{id_obra}/arquivar", response_model=ObraRead)
def arquivar_obra(id_obra: int, db: Session = Depends(obter_sessao_db)):
    """
    Marca uma obra como arquivada (invisível para o público).
    """
    obra = db.query(models.Artwork).filter(models.Artwork.id == id_obra).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra não encontrada")
    
    obra.arquivado = True
    db.commit()
    db.refresh(obra)
    return obra