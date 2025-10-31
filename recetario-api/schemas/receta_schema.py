# recetario-api/schemas/receta.py
from pydantic import BaseModel
from typing import Optional

class RecetaBase(BaseModel):
    titulo: str
    instrucciones: str
    tiempo_preparacion: Optional[int] = None
    tiempo_coccion: Optional[int] = None
    url_imagen: Optional[str] = None

class RecetaCreate(RecetaBase):
    pass

class RecetaUpdate(RecetaBase):
    pass

class RecetaOut(RecetaBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True
