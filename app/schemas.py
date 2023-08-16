# Create the Pydantic Models
from pydantic import BaseModel

class BeerBase(BaseModel):
    name: str
    abv: int

class CreateBeer(BeerBase):
    pass

class Beer(BeerBase):
    id: int

    class Config:
        orm_mode = True