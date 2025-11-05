# recetario-api/schemas/auth.py
from pydantic import BaseModel, EmailStr, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str

class Usuario(BaseModel):
    id: int
    nombre_usuario: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class UsuarioCreate(BaseModel):
    nombre_usuario: str
    email: EmailStr
    password: str

class Config:
    from_attributes = True
