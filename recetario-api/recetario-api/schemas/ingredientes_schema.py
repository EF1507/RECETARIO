# schemas/ingrediente_schema.py
from pydantic import BaseModel

# --- Schema Base ---
# Contiene los campos comunes
class IngredienteBase(BaseModel):
    nombre: str

# --- Schema de Creación (Input) ---
# Usado por el endpoint POST para crear.
# No necesita el 'id' porque la base de datos lo genera.
class IngredienteCreate(IngredienteBase):
    pass

# --- Schema de Salida (Output) ---
# Usado como 'response_model' para GET y POST.
# Envía el 'id' y el 'nombre' al cliente.
class IngredienteOut(IngredienteBase):
    id: int

    class Config:
        from_attributes = True
