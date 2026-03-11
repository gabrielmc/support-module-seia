# app/routes/processos_routes.py

import re
import logging
from fastapi import APIRouter
from app.services.processo_service import ProcessoService
from app.models.schemas.general_schemas import *

router = APIRouter(
    prefix="/processos",
    tags=["PROCESSOS & CEFIR"]
)
logger = logging.getLogger("processos")

@router.post("/processo/{identificador}")
async def alterar_status_controle_tramitacao(controle_tramitacao: str):
    logger.info(f"POST /processo")
    try:
        service = ProcessoService().removendo_status_anterior(tramitacao=controle_tramitacao)
        return service
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /processo[params] erro : {e}")
        return {"error": str(e)}

@router.post("/cefir/excluir-duplicado")
async def excluir_requerimento_duplicado(payload: ExcluirRequerimentoLogico):
    logger.info(f"POST /cefir/excluir-duplicado")
    try:
        cnpj_cpf_limpo = re.sub(r"\D", "", payload.cpf_cnpj)
        service = ProcessoService().excluir_requerimento_logicamente(
            requerente=payload.requerente,
            cpf_cnpj=cnpj_cpf_limpo,
            imovel=payload.imovel
        )
        return service
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /cefir/excluir-duplicado erro : {e}")
        return {"error": str(e)}
