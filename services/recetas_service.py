# recetario-api/services/receta.py
from sqlalchemy.orm import Session
from models.receta import Receta
from schemas.receta_schema import RecetaCreate, RecetaUpdate

def get_recetas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Receta).offset(skip).limit(limit).all()

def get_receta(db: Session, receta_id: int):
    return db.query(Receta).filter(Receta.id == receta_id).first()

def create_receta(db: Session, receta: RecetaCreate, usuario_id: int):
    db_receta = Receta(**receta.dict(), usuario_id=usuario_id)
    db.add(db_receta)
    db.commit()
    db.refresh(db_receta)
    return db_receta

def update_receta(db: Session, receta_id: int, receta_update: RecetaUpdate):
    r = get_receta(db, receta_id)
    if not r:
        return None
    for k, v in receta_update.dict(exclude_unset=True).items():
        setattr(r, k, v)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

def delete_receta(db: Session, receta_id: int):
    r = get_receta(db, receta_id)
    if not r:
        return False
    db.delete(r)
    db.commit()
    return True
