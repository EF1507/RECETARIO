# recetario-api/routers/recetas.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from schemas.receta_schema import RecetaCreate, RecetaOut, RecetaUpdate
from dependencias import get_db
from sqlalchemy.orm import Session
from services.recetas_service import get_recetas, get_receta, create_receta, update_receta, delete_receta
from services.auth_service import get_current_user
from schemas.auth_schema import Usuario as UsuarioSchema
from models.receta_ingrediente import RecetaIngrediente
from models.ingredientes import Ingrediente
from models.receta import Receta

router = APIRouter(prefix="/recetas", tags=["recetas"])

@router.get("/", response_model=List[RecetaOut])
def listar_recetas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_recetas(db, skip, limit)

@router.get("/{receta_id}", response_model=RecetaOut)
def ver_receta(receta_id: int, db: Session = Depends(get_db)):
    r = get_receta(db, receta_id)
    if not r:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return r

@router.put("/{receta_id}", response_model=RecetaOut)
def editar_receta(receta_id: int, receta: RecetaUpdate, db: Session = Depends(get_db), current_user: UsuarioSchema = Depends(get_current_user)):
    r = get_receta(db, receta_id)
    if not r:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    r2 = update_receta(db, receta_id, receta)
    return r2

@router.delete("/{receta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_receta(receta_id: int, db: Session = Depends(get_db), current_user: UsuarioSchema = Depends(get_current_user)):
    r = get_receta(db, receta_id)
    if not r:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    ok = delete_receta(db, receta_id)
    if not ok:
        raise HTTPException(status_code=500, detail="No se pudo eliminar")
    return None

@router.post("/")
def crear_receta(
    data: dict, 
    db: Session = Depends(get_db), 
    current_user: UsuarioSchema = Depends(get_current_user)
):
    # 1. Creamos la receta 
    nueva = Receta(
        titulo=data["titulo"],
        instrucciones=data["instrucciones"],
        tiempo_preparacion=data.get("tiempo_preparacion"),
        tiempo_coccion=data.get("tiempo_coccion"),
        url_imagen=data.get("url_imagen"),
        usuario_id=current_user.id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

   # 2. Asociamos los ingredientes (si hay)
    if "ingredientes" in data and data["ingredientes"]:
        
        for ingrediente_id_num in data["ingredientes"]:
            
            # Solo por seguridad, chequeamos que sea un número
            if not isinstance(ingrediente_id_num, int):
                continue

            # Creamos la relación Receta-Ingrediente
            ri = RecetaIngrediente(
                receta_id=nueva.id,
                ingrediente_id=ingrediente_id_num,
                
            )
            db.add(ri)
            
        # Hacemos un solo commit al final del loop
        db.commit()

    return {"mensaje": "Receta creada con éxito", "id": nueva.id}