# recetario-api/models/plan_semanal.py
# Imports
from sqlalchemy import Column, Integer, ForeignKey, String, Date
from config.database import Base
from sqlalchemy.orm import relationship

class PlanSemanal(Base):
    __tablename__ = "plan_semanal"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    receta_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)
    fecha_plan = Column(Date, nullable=False)
    tipo_comida = Column(String(50))

    # Relaciones (opcional pero recomendable)
    receta = relationship("Receta", back_populates="planes")
