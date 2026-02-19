# app/routes/processos_routes.py

import logging
import re
from fastapi import APIRouter
from app.services.processo_service import ProcessoService
from app.models.schemas.general_schemas import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("processos")

router = APIRouter(
    prefix="/processos",
    tags=["PROCESSOS & CEFIR"]
)

@router.post("/processo/{identificador}")
async def alterar_status_controle_tramitacao(controle_tramitacao: str):
    try:
        service = ProcessoService().removendo_status_anterior(tramitacao=controle_tramitacao)
        return service
    except Exception as e:
        print(f"Erro ao alterar status controle tramitacao: {e}")
        return {"error": str(e)}


@router.post("/cefir/excluir-duplicado")
async def excluir_requerimento_duplicado(payload: ExcluirRequerimentoLogico):
    try:
        cnpj_cpf_limpo = re.sub(r"\D", "", payload.cpf_cnpj)
        service = ProcessoService().excluir_requerimento_logicamente(
            requerente=payload.requerente,
            cpf_cnpj=cnpj_cpf_limpo,
            imovel=payload.imovel
        )
        return service
    except Exception as e:
        print(f"Erro ao excluir requerimento duplicado: {e}")
        return {"error": str(e)}
        #raise HTTPException(status_code=500, detail=str(e))
