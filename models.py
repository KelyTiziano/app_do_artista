# Import the column types we will use in the database
# Each type defines what kind of data will be stored (text, number, etc)
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey

# Import the "Base" from the database.py file
# All models (tables) inherit from this Base
from database import Base
from sqlalchemy.orm import relationship

#Association table between artworks and categories
artwork_categories = Table(
    "artwork_categories",
    Base.metadata,
    Column("artwork_id", ForeignKey("artwork.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True)
)

#category model

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

# Create the class that represents the artworks table
class Artwork(Base):
    # Table name in the database
    __tablename__ = "artworks"

    # Below we define the table columns
    # Each attribute becomes a column in the database

    # Unique ID for each artwork
    # primary_key=True → uniquely identifies the row
    # index=True → creates an index for faster searches
    id = Column(Integer, primary_key=True, index=True)

    # Name of the artwork (required)
    # nullable=False → cannot be empty
    name = Column(String, nullable=False)

    # Name of the collection (optional)
    collection = Column(String)

    # Year the artwork was created (optional)
    year = Column(Integer)

    # Indicates if the artwork is archived (invisible to the public)
    # Default is False (visible)
    archived = Column(Boolean, default=False)

    # Image path (URL or saved file name)
    image_url = Column(String)

    # Many-to-many relationship with Category
    categories = relationship(
        "Category", 
        secondary=artwork_categories,
        backref = "artworks" # correction from obras.id to arwork.id, stop mistake from foreing key inexistent
    )