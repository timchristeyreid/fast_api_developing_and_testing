from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


app = FastAPI()


# Defining an initial test route
@app.get("/")
def home():
    return {"message":"hello"}


# Create the database tables
models.Base.metadata.create_all(bind=engine)


# Dependency will create a new SQLAlchemy SessionLocal for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create-beer/", response_model=schemas.Beer)
def create_beer(beer: schemas.CreateBeer, db: Session = Depends(get_db)):
    db_beer = crud.get_beer_by_name(db, name=beer.name )
    if db_beer:
        raise HTTPException(status_code=400, detail="Beer already exists")
    return crud.create_beer(db=db, beer=beer)


@app.get("/beer/{id}", response_model=schemas.Beer)
def get_beer(id:int, db: Session = Depends(get_db)):
    db_beer = crud.get_beer(db, id=id)
    if db_beer is None:
        raise HTTPException(status_code=404, detail="Beer does not exist")
    return db_beer