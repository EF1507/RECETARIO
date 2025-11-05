# recetario-api/dependencias.py

# --- Imports ---
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# Importamos AMBOS motores desde tu configuración
# 'engine' es para el código síncrono (el antiguo)
# 'async_engine' es para el código asíncrono (el nuevo)
from config.database import Base, engine, async_engine

# -------------------------------------------------
# --- Dependencia Síncrona (La que ya tenías) ---
# -------------------------------------------------
# No se toca. Sigue funcionando para las rutas antiguas.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------
# --- Dependencia Asíncrona (La nueva) ---
# ---------------------------------------------------
# Esta es la que usarán tus nuevas rutas (como planificador.py)

# 1. Creamos el "fabricante" de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# 2. Creamos la dependencia de FastAPI asíncrona
async def get_async_db():
    """
    Dependencia de FastAPI para obtener una AsyncSession.
    Se asegura de cerrar la sesión al finalizar.
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()