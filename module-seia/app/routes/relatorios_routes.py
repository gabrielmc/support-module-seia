# app/routes/relatorios_routes.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/relatorios",
    tags=["RELATÓRIOS"]
)

@router.get("/")
def gerar_relatorio():
    return {"modulo": "RELATÓRIOS"}
