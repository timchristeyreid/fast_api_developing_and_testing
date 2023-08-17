''' 
Altering a database for testing:

This file sets up a testing database - this is a temporary database only for the tests.

'''

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app, get_db

engine = create_engine(
    'sqlite://', 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Create dependency override 

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Test code as usual

client = TestClient(app)

def test_create_beer():
    response = client.post(
        "/create-beer/",
        json={
        "id": 1, 
        "name": "Lager", 
        "abv": 4}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Lager"
    assert "id" in data
    assert data["abv"] == 4
    id = data["id"]

    response = client.get(f"/beer/{id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Lager"
    assert data["id"] == id

def test_create_existing_beer():
    response = client.post(
        "/create-beer/",
        json={
        "id": 1, 
        "name": "Lager", 
        "abv": 4}
    )
    assert response.status_code == 400
    assert response.json() == {"detail":"Beer already exists"}

def test_read_beer():
    response = client.get("/beer/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1, 
        "name": "Lager", 
        "abv": 4
    }

def test_read_invalid_beer():
    response = client.get("/beer/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Beer does not exist"}