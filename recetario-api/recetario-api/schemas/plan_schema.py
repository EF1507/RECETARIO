# recetario-api/schemas/plan_schema.py

from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List

# --- Schemas para el Plan Semanal ---

class PlanSemanalBase(BaseModel):
    fecha_plan: date
    tipo_comida: str | None = None
    receta_id: int

class PlanSemanalCreate(PlanSemanalBase):
    pass # Los datos para crear son iguales a la base

class PlanSemanalDB(PlanSemanalBase):
    id: int
    usuario_id: int

    model_config = ConfigDict(from_attributes=True)

# --- Schemas para la Lista de Compras ---

class ListaComprasItem(BaseModel):
    ingrediente: str
    cantidad_total: float
    unidad: str


    class Config:
     from_attributes = True
