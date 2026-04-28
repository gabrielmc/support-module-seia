# app/routes/segurancas_routes.py

import logging
from fastapi import APIRouter
from app.services.monitoramento_service import MonitoramentoService
from app.core.dependencies import CommonAuth

router = APIRouter(
    prefix="/monitoramentos",
    tags=["MONITORAMENTO"]
)
logger = logging.getLogger("monitoramentos")

@router.get("/monitoramento-memoria-jboss")
async def executar_scripts_zip(auth: bool = CommonAuth):
    logger.info(f"GET /monitoramento-memoria-jboss")
    try:
        resultado = MonitoramentoService.monitorar_memoria_jboss()
        return {"sucesso": True, "resultado": resultado}
    except Exception as e:
        logger.warning(f"EXCEPTION - GET - /monitoramento-memoria-jboss erro : {e}")
        return {"sucesso": False, "error": str(e)}

@router.get("/monitoramento-atualizacao-banco")
async def executar_scripts_zip(auth: bool = CommonAuth):
    logger.info(f"GET /monitoramento-atualizacao-banco")
    try:
        resultado = MonitoramentoService.monitorar_atualizacao_banco()
        return {"sucesso": True, "resultado": resultado}
    except Exception as e:
        logger.warning(f"EXCEPTION - GET - /monitoramento-atualizacao-banco erro : {e}")
        return {"sucesso": False, "error": str(e)}