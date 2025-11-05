# recetario-api/routers/planificador.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from dependencias import get_async_db
from services.auth_service import get_current_user
from services.plan_service import generar_lista_de_compras, crear_plan_semanal
from datetime import date, timedelta
from schemas.auth_schema import Usuario as UsuarioSchema
from schemas.plan_schema import PlanSemanalCreate, PlanSemanalDB
from dependencias import get_async_db
router = APIRouter(prefix="/planificador", tags=["planificador"])

@router.get("/ingredientes-semana", tags=["planificador"])
async def ingredientes_semana(
    db: AsyncSession = Depends(get_async_db),
    # 👇 ¡ESTA ES LA CORRECCIÓN! 👇
    # Usamos el token para saber quién es el usuario
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Devuelve la lista consolidada de ingredientes para la semana actual
    DEL USUARIO AUTENTICADO.
    """
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # lunes
    fin_semana = inicio_semana + timedelta(days=6)       # domingo

    # 👇 Usamos el ID del usuario del token
    lista = await generar_lista_de_compras(
        db, 
        current_user.id,  # <-- Ya no es '1', es el ID del usuario real
        inicio_semana, 
        fin_semana
    )

    if not lista:
        # Esto es correcto, Axios lo manejará como un error
        raise HTTPException(
            status_code=404, 
            detail="No hay recetas planificadas esta semana."
        )

    return lista

@router.post("/", response_model=PlanSemanalDB, status_code=status.HTTP_201_CREATED, tags=["planificador"])
async def agregar_receta_al_plan(
    plan_in: PlanSemanalCreate, # (Este nombre estaba bien)
    db: AsyncSession = Depends(get_async_db),
    current_user: UsuarioSchema = Depends(get_current_user)
):
    """
    Agrega una receta existente al plan semanal del usuario autenticado.
    """
    
    nuevo_plan = await crear_plan_semanal(
        db=db, 
        plan_in=plan_in, 
        usuario_id=current_user.id
    )
    
    return nuevo_plan