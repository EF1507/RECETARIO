# recetario-api/models/receta_ingrediente.py
# Imports
from sqlalchemy import Column, Integer, ForeignKey, Float, String
from config.database import Base
from sqlalchemy.orm import relationship

class RecetaIngrediente(Base):
    __tablename__ = "receta_ingredientes"

    receta_id = Column(Integer, ForeignKey("recetas.id"), primary_key=True)
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), primary_key=True)

    receta = relationship("Receta", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente")
