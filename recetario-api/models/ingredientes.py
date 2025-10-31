from sqlalchemy import Column, Integer, String
from config.database import Base

class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
