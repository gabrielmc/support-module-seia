# app/routes/segurancas_routes.py

import logging
from fastapi import APIRouter
from app.services.seguranca_service import SegurancaService
from app.models.schemas.general_schemas import ListaUsuariosEmail, ListaUsuariosCPF

router = APIRouter(
    prefix="/seguranca",
    tags=["SEGURANÇA"]
)
logger = logging.getLogger("seguranca")

@router.post("/administrativo/{nome_usuario}")
async def up_perfil_administrativo(nome_usuario: str):
    try:
        service = SegurancaService().atualizar_perfil(nome_usuario)
        return service
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /administrativo/[params] : {e}")
        print(f"Erro ao atualizar perfil administrativo: {e}")
        return {"error": str(e)}

@router.post("/inclui-email")
async def incluir_email_usuario(payload: ListaUsuariosEmail):
    try:
        service = SegurancaService().incluir_email_usuario(payload.usuarios)
        return service
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /inclui-email erro : {e}")
        print(f"Erro ao incluir email do usuário: {e}")
        return {"sucesso": False, "error": str(e)}

@router.post("/gerar-script-email-cpf")
async def gerar_script(payload: ListaUsuariosCPF):
    try:
        file_path = SegurancaService().gerar_script_email_por_cpf(payload.usuarios)
        return {
            "sucesso": True,
            "arquivo_gerado": file_path
        }
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /gerar-script-email-cpf erro : {e}")
        print(f"Erro ao gerar script de email por CPF: {e}")
        return {"sucesso": False, "error": str(e)}
