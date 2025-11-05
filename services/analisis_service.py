# recetario-api/services/analisis_service.py

import matplotlib.pyplot as plt
import io # Used to save the plot to memory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, desc

from models import models

async def generar_grafico_ingredientes_usados(db: AsyncSession, usuario_id: int):
    """
    Genera un gráfico de barras con los 10 ingredientes más usados por el usuario.
    Devuelve los bytes de la imagen PNG.
    """
    # Consulta para contar la frecuencia de cada ingrediente para el usuario
    query = (
        select(
            models.Ingrediente.nombre, 
            func.count(models.RecetaIngrediente.ingrediente_id).label('conteo')
        )
        .join(models.RecetaIngrediente, models.Ingrediente.id == models.RecetaIngrediente.ingrediente_id)
        .join(models.Receta, models.Receta.id == models.RecetaIngrediente.receta_id)
        .where(models.Receta.usuario_id == usuario_id)
        .group_by(models.Ingrediente.nombre)
        .order_by(desc('conteo'))
        .limit(10) # Top 10
    )
    
    result = await db.execute(query)
    data = result.fetchall()
    
    if not data:
        return None # No data to plot

    nombres = [row[0] for row in data]
    conteos = [row[1] for row in data]

    # --- Generación del gráfico con Matplotlib ---
    plt.figure(figsize=(10, 6)) # Tamaño de la figura
    plt.barh(nombres, conteos, color='skyblue') # Gráfico de barras horizontales
    plt.xlabel('Número de Recetas en las que aparece')
    plt.ylabel('Ingrediente')
    plt.title('Top 10 Ingredientes Más Usados')
    plt.gca().invert_yaxis() # Poner el más usado arriba
    plt.tight_layout() # Ajusta el layout para que no se corten las etiquetas

    # Guardar el gráfico en un buffer de memoria en formato PNG
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0) # Rebobinar el buffer al principio
    plt.close() # Cerrar la figura para liberar memoria
    
    return buf.getvalue() # Devolver los bytes de la imagen