from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models, schemas

def get_beer(db: Session, id:int):
    return db.query(models.Beer).filter(models.Beer.id == id).first()

def get_beer_by_name(db: Session, name:str):
    return db.query(models.Beer).filter(models.Beer.name == name).first()

def create_beer(db: Session, beer:schemas.CreateBeer):
    db_beer = models.Beer(**beer.dict())
    db.add(db_beer)
    db.commit()
    db.refresh(db_beer)
    return db_beer
# the **beer.dict() is used instead of passing each of the keyword arguments to Beer and reading each one from the pydantic model