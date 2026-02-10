# app/routes/segurancas_routes.py

from fastapi import APIRouter
from app.services.seguranca_service import SegurancaService

router = APIRouter(
    prefix="/seguranca",
    tags=["SEGURANÇA"]
)

@router.post("/administrativo/{nome_usuario}")
async def up_perfil_administrativo(nome_usuario: str):
    try:
        service = SegurancaService().atualizar_perfil(nome_usuario)
        return service
    except Exception as e:
        print(f"Erro ao atualizar perfil administrativo: {e}")
        return {"error": str(e)}
