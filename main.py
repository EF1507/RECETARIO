from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, Base
import models.usuario, models.receta, models.ingredientes
from routers import auth, recetas, ingredientes, planificador, estadisticas
from routers.auth_register import router as register_router

app = FastAPI(title="Recetario API")

# Habilitar CORS
origins = [
    "http://localhost",
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(auth.router)
app.include_router(register_router)
app.include_router(recetas.router)
app.include_router(ingredientes.router)
app.include_router(planificador.router)
app.include_router(estadisticas.router)

