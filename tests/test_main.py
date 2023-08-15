from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_beer():
    response = client.post(
        "/create-beer/",
        json={
            "id": 2, 
            "name": "Lager", 
            "abv": 4}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 2, 
        "name": "Lager", 
        "abv": 4}

def test_get_beer_by_id():
    response = client.get("/beer/1")
    assert response.status_code == 200
    assert response.json() == {
            "id":1,
            "name":"IPA",
            "abv":5
        }

def test_create_invalid_existing_beer():
    response = client.post(
        "/create-beer/",
        json={
            "id": 1, 
            "name": "IPA", 
            "abv": 5}
    )
    assert response.status_code == 400
    assert response.json() == {"detail":"Beer ID already exists"}