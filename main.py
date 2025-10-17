from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
from schemas import ArtworkCreate, ArtworkRead, CategoryRead
from typing import List
 
# Create the FastAPI application
app = FastAPI()

# Create tables in the database if they do not exist yet
# This line ensures that all tables defined in models.py
# exist in the database. If they do not exist, they will be created.
models.Base.metadata.create_all(bind=engine)


# DATABASE DEPENDENCY

def get_db_session():

    """
        Creates a database session and ensures it will be closed after use
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TEST ROUTE

@app.get("/")
def main_route():
    """Initial test route"""
    return {"message": " Visual Artist API is working!"}


# LIST ALL ARTWORKS

@app.get("/artworks", response_model=List[ArtworkRead])
def list_all_artworks(db: Session = Depends(get_db_session)):
    
    """
        Returns all registered artworks
    """
    artworks = db.query(models.Artwork).all()
    return artworks

# LIST ARTWORKS VISIBLE TO THE PUBLIC

@app.get("/artworks/visible", response_model=List[ArtworkRead])
def list_visible_artworks(db: Session = Depends(get_db_session)):
    """
    Returns only the artworks that are NOT archived (archived = False),
    i.e., visible to the general public.
    """
    visible_artworks = db.query(models.Artwork).filter(models.Artwork.archived == False).all()
    return visible_artworks


# ADD A NEW ARTWORK

@app.post("/artworks", response_model=ArtworkRead, status_code=201)
def register_artwork(artwork: ArtworkCreate, db: Session = Depends(get_db_session)):
    """
    Adds a new artwork to the database.
    Receives a JSON with all required fields:
    {
        "name": "Name of the artwork",
        "collection": "Name of the collection",
        "year": 2025,
        "categories_ids": [1,2,3],
        "image_url": "path/to/image"
    }
    """

    categories = db.query(models.Category).filter(models.Category.id.in_(artwork.category_ids)).all()
    if len(categories) != len(artwork.category_ids):
        raise HTTPException(status_code=404, detail="One or more categories not found")
    
    #create artwork
    new_artwork = models.Artwork(
        name=artwork.name,
        collection=artwork.collection,
        year=artwork.year,
        categories=categories,
        image_url=artwork.image_url
    )
    db.add(new_artwork)
    db.commit()
    db.refresh(new_artwork)  # gets the generated ID
    return new_artwork

    # ARCHIVE AN ARTWORK
@app.put("/artworks/{artwork_id}/archive", response_model=ArtworkRead)
def archive_artwork(artwork_id: int, db: Session = Depends(get_db_session)):
    
    """
    Marks an artwork as archived (invisible to the public).
    """

    artwork = db.query(models.Artwork).filter(models.Artwork.id == artwork_id).first()
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")
    
    artwork.archived = True
    db.commit()
    db.refresh(artwork)
    return artwork
