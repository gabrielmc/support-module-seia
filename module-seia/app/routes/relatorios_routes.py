# app/routes/relatorios_routes.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/relatorios",
    tags=["RELATÓRIOS"]
)

@router.get("/relatorios")
def gerar_relatorio():
    return {"modulo": "RELATÓRIOS"}
