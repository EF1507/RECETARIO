from fastapi import APIRouter, Depends, HTTPException, status
from schemas.auth_schema import UsuarioCreate, Usuario
from services.auth_service import get_password_hash
from dependencias import get_db
from sqlalchemy.orm import Session
from models.usuario import Usuario as UsuarioModel

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    # validar unicidad
    if db.query(UsuarioModel).filter(
        (UsuarioModel.nombre_usuario == user.nombre_usuario) | (UsuarioModel.email == user.email)
    ).first():
        raise HTTPException(status_code=400, detail="Usuario o email ya existe")
    new = UsuarioModel(
        nombre_usuario=user.nombre_usuario,
        email=user.email,
        contrasena_hash=get_password_hash(user.password),
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new
