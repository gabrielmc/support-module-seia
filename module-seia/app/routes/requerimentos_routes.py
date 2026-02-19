# app/routes/requerimentos_routes.py

import logging
from fastapi import APIRouter
from app.models.schemas.general_schemas import *
from app.services.repflor_service import RepflorService

router = APIRouter(
    prefix="/requerimentos",
    tags=["REQUERIMENTOS"]
)
logger = logging.getLogger("requerimentos")

@router.post("/repflor/{identificador}")
async def up_requerimentos_repflor(identificador: str):
    logger.info(f"POST /repflor")
    try:
        identificador_formatted = identificador+"/INEMA/REPFLOR"
        service = RepflorService().processar(identificador_formatted)
        return service
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /repflor[params] erro : {e}")
        print(f"Erro ao atualizar repflors: {e}")
        return {"error": str(e)}
    
@router.get("/repflor-status/{identificador}")
async def consulta_status_repflor(identificador: str):
    logger.info(f"GET /repflor-status")
    try:
        identificador_formatted = identificador+"/INEMA/REPFLOR"
        service = RepflorService().consultar_status(identificador_formatted)
        return service
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /repflor-status erro : {e}")
        print(f"Erro ao consultar status repflor: {e}")
        return {"error": str(e)}
