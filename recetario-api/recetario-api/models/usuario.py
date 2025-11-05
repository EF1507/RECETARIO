# recetario-api/models/usuario.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from config.database import Base
from sqlalchemy.orm import relationship
from models.receta import Receta

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasena_hash = Column(String(255), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())

    recetas = relationship("Receta", back_populates="autor")
