# app/routes/segurancas_routes.py

import logging
from fastapi import APIRouter
from app.services.monitoramento_service import MonitoramentoService


router = APIRouter(
    prefix="/monitoramentos",
    tags=["MONITORAMENTO"]
)
logger = logging.getLogger("monitoramentos")

@router.get("/monitoramento-memoria-jboss")
async def executar_scripts_zip():
    logger.info(f"GET /monitoramento-memoria-jboss")
    try:
        resultado = MonitoramentoService.monitorar_memoria_jboss()
        return {"sucesso": True, "resultado": resultado}
    except Exception as e:
        logger.warning(f"EXCEPTION - GET - /monitoramento-memoria-jboss erro : {e}")
        print(f"Erro ao executar : {e}")
        return {"sucesso": False, "error": str(e)}