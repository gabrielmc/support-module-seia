# app/routes/segurancas_routes.py

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.seguranca_service import SegurancaService
from app.models.schemas.general_schemas import ListaUsuariosEmail, ListaUsuariosCPF, UsuarioPerfil

router = APIRouter(
    prefix="/seguranca",
    tags=["SEGURANÇA"]
)
logger = logging.getLogger("seguranca")

@router.post("/alterar-perfil")
async def up_perfil_administrativo(payload: UsuarioPerfil):
    logger.info(f"POST /alterar-perfil")
    try:
        service = SegurancaService().atualizar_perfil(payload.usuario, payload.perfil)
        return service
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /alterar-perfil/[params] : {e}")
        return {"error": str(e)}

@router.post("/inclui-email")
async def incluir_email_usuario(payload: ListaUsuariosEmail):
    logger.info(f"POST /inclui-email")
    try:
        service = SegurancaService().incluir_email_usuario(payload.usuarios)
        return service
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /inclui-email erro : {e}")
        return {"sucesso": False, "error": str(e)}

@router.post("/gerar-script-email-cpf")
async def gerar_script(payload: ListaUsuariosCPF):
    logger.info(f"POST /gerar-script-email-cpf")
    try:
        file_path = SegurancaService().gerar_script_email_por_cpf(payload.usuarios)
        return {
            "sucesso": True,
            "arquivo_gerado": file_path
        }
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /gerar-script-email-cpf erro : {e}")
        return {"sucesso": False, "error": str(e)}
