from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencias import get_db
from models.receta import Receta
from models.plan_semanal import PlanSemanal
import matplotlib.pyplot as plt
import io, base64

router = APIRouter(prefix="/estadisticas", tags=["estadisticas"])

@router.get("/ingredientes-populares")
def ingredientes_populares(db: Session = Depends(get_db)):
    # Generar gráfico de ingredientes más usados
    recetas = db.query(Receta).all()
    conteo = {}
    for r in recetas:
        for ing in r.ingredientes:
            conteo[ing.nombre] = conteo.get(ing.nombre, 0) + 1
    if not conteo:
        return {"mensaje": "No hay datos."}

    plt.figure(figsize=(6,4))
    plt.bar(conteo.keys(), conteo.values())
    plt.xticks(rotation=45, ha="right")
    plt.title("Ingredientes más usados")

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode("utf-8")
    return {"imagen": f"data:image/png;base64,{img}"}
