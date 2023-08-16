# Create the database models from the Base class

from sqlalchemy import Column, Integer, String

from .database import Base

class Beer(Base):
    __tablename__ = "beers"

# Create model class attributes/columns - Each attribute represents a column in the DB
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    abv = Column(Integer)