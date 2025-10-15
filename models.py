# Import the column types we will use in the database
# Each type defines what kind of data will be stored (text, number, etc)
from sqlalchemy import Column, Integer, String, Boolean

# Import the "Base" from the database.py file
# All models (tables) inherit from this Base
from database import Base

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

    # Category of the artwork (e.g., "abstract", "landscape", etc.)
    category = Column(String)

    # Indicates if the artwork is archived (invisible to the public)
    # Default is False (visible)
    archived = Column(Boolean, default=False)

    # Image path (URL or saved file name)
    image_url = Column(String)
