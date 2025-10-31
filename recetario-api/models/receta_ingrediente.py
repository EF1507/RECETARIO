# recetario-api/models/receta_ingrediente.py
# Imports
from sqlalchemy import Column, Integer, ForeignKey, Float, String
from config.database import Base
from sqlalchemy.orm import relationship

class RecetaIngrediente(Base):
    __tablename__ = "receta_ingredientes"

    id = Column(Integer, primary_key=True)
    receta_id = Column(Integer, ForeignKey("recetas.id"))
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"))
    cantidad = Column(Float, nullable=False)
    unidad = Column(String(20))  # ← importante para que Pandas pueda agrupar

    receta = relationship("Receta", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente")
