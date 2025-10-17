from pydantic import BaseModel
from typing import Optional, List

# Schema to creat a category
class CategoryCreate(BaseModel):
    name: str  # category name (required)

# Schema to read a category
class CategoryRead(BaseModel):
    id: int
    name: str

    class Config:
        model_config = dict(from_attributes=True)

# Schema to create an artwork
class ArtworkCreate(BaseModel):
    name: str            # Name of the artwork (required)
    collection: str      # Name of the collection (required)
    year: int            # Year of creation (required)
    category_ids: List[int]        # list of Category Ids for the artwork
    image_url: str       # Path or URL of the image (required)

# Schema to return an artwork
class ArtworkRead(BaseModel):
    id: int
    name: str
    collection: str
    year: int
    categories: List[CategoryRead]#List of categories associated
    archived: bool
    image_url: str

    class Config:
        model_config = dict(from_attributes=True)