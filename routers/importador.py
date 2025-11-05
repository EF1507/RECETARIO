# recetario-api/routers/importador.py

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from dependencias import get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Annotated

from models import models
from services import auth_service, scraping_service # 'scraping_service' ahora tiene el nuevo código
from schemas.receta_schema import RecetaCreate 
from services.recetas_service import RecetaService

router = APIRouter(
    prefix="/importar",
    tags=["Importador (Web Scraping)"]
)

class URLImportRequest(BaseModel):
    url: str

class IngredienteImportado(BaseModel):
    nombre: str
    cantidad: float
    unidad: str

class RecetaImportadaResponse(BaseModel):
    titulo: str
    instrucciones: str
    ingredientes: List[IngredienteImportado]

@router.post("/", response_model=RecetaImportadaResponse)
async def importar_receta_desde_url(
    request: URLImportRequest,
    current_user: Annotated[models.Usuario, Depends(auth_service.get_current_user)]
):
    """
    Recibe una URL (ej. de RecetasGratis.net), hace scraping
    y devuelve los datos de la receta listos para el formulario.
    """
    
    if "recetasgratis.net" not in request.url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Por ahora, solo se pueden importar recetas de 'recetasgratis.net'"
        )

    # Llamamos a la nueva función de scraping
    datos_receta = scraping_service.scrape_recetas_gratis(request.url)
    
    if datos_receta is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo procesar la receta desde esa URL."
        )
        
    return datos_receta



@router.post("/guardar-receta-importada", response_model=RecetaImportadaResponse)
async def guardar_receta_importada(
    receta_scrapeada: RecetaImportadaResponse,
    current_user: Annotated[models.Usuario, Depends(auth_service.get_current_user)],
    db: AsyncSession = Depends(get_db_session)
):
    """
    Recibe los datos scrapeados, busca/crea los ingredientes
    y finalmente guarda la nueva receta en la base de datos.
    """
    service = RecetaService(db)
    receta_guardada = await service.save_imported_receta(
        receta_scrapeada=receta_scrapeada,
        usuario_id=current_user.id
    )
    return receta_guardada