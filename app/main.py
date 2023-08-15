from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Defining an initial test route
@app.get("/")
def home():
    return {"message":"hello"}

#storing all the beers 
db = {
    1: {"id": 1, "name": "IPA", "abv": 5}
}


#Creating a class to be used in request body
class Beer(BaseModel):
    id: int
    name: str
    abv: int

@app.post("/create-beer/", response_model=Beer)
def create_beer(beer: Beer):
    if beer.id in db:
        raise HTTPException(status_code=400, detail="Beer ID already exists")
    db[beer.id] = beer
    return beer


@app.get("/beer/{id}", response_model=Beer)
def get_beer(id:int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Beer does not exist")
    return db[id]