from pydantic import BaseModel
from typing import Optional

# Schema to create an artwork
class ArtworkCreate(BaseModel):
    name: str            # Name of the artwork (required)
    collection: str      # Name of the collection (required)
    year: int            # Year of creation (required)
    category: str        # Category of the artwork (required)
    image_url: str       # Path or URL of the image (required)

# Schema to return an artwork
class ArtworkRead(BaseModel):
    id: int
    name: str
    collection: str
    year: int
    category: str
    archived: bool
    image_url: str

    class Config:
        orm_mode = True
