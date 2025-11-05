# recetario-api/services/plan_service.py

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from datetime import date
import models
import schemas.plan_schema as plan_schema
from dependencias import get_async_db

async def generar_lista_de_compras(
    db: AsyncSession, 
    usuario_id: int, 
    fecha_inicio: date, 
    fecha_fin: date
):
    """
    Genera una lista de compras consolidada para un usuario y un rango de fechas.
    El procesamiento lo hacemos con Pandas.
    """

    # 1. CONSULTA: Traemos todos los ingredientes de todas las recetas
    #    planificadas por el usuario en el rango de fechas.
    query = (
    select(models.Ingrediente.nombre)
    .join(models.RecetaIngrediente, models.Ingrediente.id == models.RecetaIngrediente.ingrediente_id)
    .join(models.Receta, models.Receta.id == models.RecetaIngrediente.receta_id)
    .join(models.PlanSemanal, models.PlanSemanal.receta_id == models.Receta.id)
    .where(
        models.PlanSemanal.usuario_id == usuario_id,
        models.PlanSemanal.fecha_plan.between(fecha_inicio, fecha_fin)
    )
    )

    result = await db.execute(query)
    ingredientes_db = result.fetchall()

    # Si no hay ingredientes, devolvemos una lista vacía
    if not ingredientes_db:
        return []

    # 2. accion de PANDAS:
    #    Creamos un DataFrame de Pandas con los resultados de la consulta
    df = pd.DataFrame(ingredientes_db, columns=['ingrediente'])

    #    Agrupo por 'ingrediente' y elimino duplicados
    df_unicos = df.drop_duplicates(subset=['ingrediente']).sort_values(by='ingrediente').reset_index(drop=True)

    # === Solo dejamos la columna 'ingrediente'
    df_limpio = df_unicos[['ingrediente']]

    # === Convertimos a lista de diccionarios
    return df_limpio.to_dict(orient='records')

async def crear_plan_semanal(
    db: AsyncSession, 
    plan_in: plan_schema.PlanSemanalCreate, 
    usuario_id: int
) -> models.PlanSemanal:
    """
    Crea una nueva entrada en el plan semanal para un usuario.
    """
    
    # Creamos el objeto del modelo SQLAlchemy
    db_plan = models.PlanSemanal(
        usuario_id=usuario_id,
        receta_id=plan_in.receta_id,
        fecha_plan=plan_in.fecha_plan,
        tipo_comida=plan_in.tipo_comida
    )
    
    # Añadimos, guardamos (commit) y refrescamos
    db.add(db_plan)
    await db.commit()
    await db.refresh(db_plan)
    
    return db_plan