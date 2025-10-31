# routers/ingredientes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencias import get_db
from models.ingredientes import Ingrediente
from schemas.ingredientes_schema import IngredienteCreate, IngredienteOut
from services.auth_service import get_current_user
from schemas.auth_schema import Usuario as UsuarioSchema

router = APIRouter(prefix="/ingredientes", tags=["ingredientes"])

@router.get("/", response_model=list[IngredienteOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Ingrediente).all()

@router.post("/", response_model=IngredienteOut)
def crear(ing: IngredienteCreate, db: Session = Depends(get_db)):
    nuevo = Ingrediente(nombre=ing.nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
