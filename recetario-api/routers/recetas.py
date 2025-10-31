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
    # opcional: verificar que current_user.id == r.usuario_id si querés permisos por autor
    r2 = update_receta(db, receta_id, receta)
    return r2

@router.delete("/{receta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_receta(receta_id: int, db: Session = Depends(get_db), current_user: UsuarioSchema = Depends(get_current_user)):
    r = get_receta(db, receta_id)
    if not r:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    # opcional: verificar owner
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
    # 1. Creamos la receta (esto ya estaba bien)
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

    # -----------------------------------------------------------------
    # 🔹 (AQUÍ ESTÁ EL CÓDIGO CORREGIDO) 🔹
    # -----------------------------------------------------------------
    # Vincular ingredientes si vienen en el payload
    if "ingredientes" in data and data["ingredientes"]:
        
        # Iteramos sobre la lista de NÚMEROS (IDs) que nos enviaste.
        # ej: [1, 2, 3]
        for ingrediente_id_num in data["ingredientes"]:
            
            # Solo por seguridad, chequeamos que sea un número
            if not isinstance(ingrediente_id_num, int):
                continue # Si no es un int, lo ignoramos

            # Creamos la relación Receta-Ingrediente
            # Asumimos que el ID (ej: 1) ya existe en tu tabla 'ingredientes'
            ri = RecetaIngrediente(
                receta_id=nueva.id,
                ingrediente_id=ingrediente_id_num,
                
                # ------ ¡LA SOLUCIÓN! ------
                # Ponemos valores por defecto para que la BD no falle
                # (ya que tu columna 'cantidad' es 'nullable=False')
                cantidad=1.0, 
                unidad="N/A" # O "unidad", "s/d", etc.
            )
            db.add(ri)
            
        # Hacemos un solo commit al final del loop
        db.commit()

    return {"mensaje": "Receta creada con éxito", "id": nueva.id}