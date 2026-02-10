# app/routes/processos_routes.py

from fastapi import APIRouter
from app.services.processo_service import ProcessoService

router = APIRouter(
    prefix="/processos",
    tags=["PROCESSO"]
)

@router.post("/processo/{identificador}")
async def alterar_status_controle_tramitacao(controle_tramitacao: str):
    try:
        service = ProcessoService().removendo_status_anterior(tramitacao=controle_tramitacao)
        return service
    except Exception as e:
        print(f"Erro ao alterar status controle tramitacao: {e}")
        return {"error": str(e)}
