from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db_session  # Import the FastAPI app and DB dependency
from database import Base, engine
import models
import pytest

@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    # search all tables before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # optional: clean after test
    Base.metadata.drop_all(bind=engine)



# Temporary file
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_db.db"  


engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Create all tables in the test database
Base.metadata.create_all(bind=engine)

# Override the database dependency
def override_get_db():

    """
    This function overrides the get_db_session dependency
    so that FastAPI endpoints use the test database instead of the real one.
    """

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_session] = override_get_db

# Test client
client = TestClient(app)

#helper function to create categories for tests
def create_categories(db):
    cat1 = models.Category(name = "Modern")
    cat2 = models.Category(name = "Abstract")
    cat3 = models.Category(name = "Psycodelic")
    db.add_all([cat1,cat2,cat3])#add all instances in session
    db.commit() #save in db
    db.refresh(cat1)#db fresh update each instance to get automatically generated ids
    db.refresh(cat2)
    db.refresh(cat3)
    return [cat1, cat2, cat3]


def test_read_root():

    """
    Test that the root endpoint "/" returns a success message.
    """

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": " Visual Artist API is working!"}

# Test adding a new artwork with multiple categories.

def test_create_artwork_with_categories():

   #first, create categories in test DB

    db = TestingSessionLocal()
    categories = create_categories(db)#cria modern, abstract and psycodelic
    db.close()

    data = {
        "name": "Starry Night",
        "collection": "Van Gogh",
        "year": 1889,
        "category_ids": [categories[0].id, categories[1].id, categories[2].id],
        "image_url": "path/to/image.jpg"
    }
    response = client.post("/artworks", json=data)
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["name"] == data["name"]
    assert json_response["archived"] is False
    assert len(json_response["categories"]) == 3
    assert {cat["name"] for cat in json_response["categories"]} == {"Modern", "Abstract", "Psycodelic"}

# test listing all artworks
def test_list_artworks():

    response = client.get("/artworks")
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, list)
    assert len(json_response) 0 >= 1

# test archiving an artwork
def test_archived_artwork():

    #create categories for the artwork
    db = TestingSessionLocal()
    categories = create_categories(db)
    db.close()
    

    response_create = client.post(
        "/artworks",
        json={
            "name": "Artwork to Archive",
            "collection": "Collection A",
            "year": 2024,
            "category_ids": [categories[0].id],
            "image_url": "archive_image.png"
        }
    )
    assert response_create.status_code == 201
    artwork_id = response_create.json()["id"]

    response_archive = client.put(f"/artworks/{artwork_id}/archive")
    assert response_archive.status_code == 200
    archived_artwork = response_archive.json()
    assert archived_artwork["id"] == artwork_id
    assert archived_artwork["archived"] is True
