# app/routes/relatorios_routes.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/consultas",
    tags=["CONSULTAS"]
)

@router.get("/checkBoletosProcessados")
def check_boletos_processados_Onsistema():
    return {"modulo": "CONSULTAS"}