# recetario-api/models/receta.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from config.database import Base
from sqlalchemy.orm import relationship
from models.receta_ingrediente import RecetaIngrediente
class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    titulo = Column(String(255), nullable=False)
    instrucciones = Column(Text, nullable=False)
    tiempo_preparacion = Column(Integer, nullable=True)
    tiempo_coccion = Column(Integer, nullable=True)
    url_imagen = Column(String(255), nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    planes = relationship("PlanSemanal", back_populates="receta")

    autor = relationship("Usuario", back_populates="recetas")
    ingredientes = relationship("RecetaIngrediente", back_populates="receta", cascade="all, delete-orphan")
