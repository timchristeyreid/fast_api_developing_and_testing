from starlette.testclient import TestClient

import json

from app.main import app

client = TestClient(app)

def test_create_beer():
    ''' Tests the create_beer function with a valid input'''
    test_request_payload = {
            "id": 4, 
            "name": "Lager", 
            "abv": 4
            }
    response = client.post(
        "/create-beer/", content=
        json.dumps(test_request_payload)
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 4, 
        "name": "Lager", 
        "abv": 4}

def test_get_beer_by_id():
    response = client.get("/beer/1")   
    assert response.status_code == 200
    assert response.json() == {
            "id":1,
            "name":"string",
            "abv":0
        }

#def test_create_invalid_existing_beer():
    #response = client.post(
        #"/create-beer/",
        #json={
            #"id": 1, 
            #"name": "IPA", 
            #"abv": 5}
    #)
    #assert response.status_code == 400
    #assert response.json() == {"detail":"Beer ID already exists"}

def test_get_beer_invalid_id():
    response = client.get("/beer/10")
    assert response.status_code == 404
    assert response.json() == {"detail":"Beer does not exist"}