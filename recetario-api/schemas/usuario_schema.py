from pydantic import BaseModel, ConfigDict

class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str

