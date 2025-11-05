from pydantic import BaseModel, ConfigDict

class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str


class Usuario(BaseModel):
    id: int
    nombre_usuario: str 
    email: str
    model_config = ConfigDict(from_attributes=True)
    from_attributes = True
        
    class Config:
      from_attributes = True
