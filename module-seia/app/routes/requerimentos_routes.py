# app/routes/requerimentos_routes.py

from fastapi import APIRouter
from app.services.repflor_service import RepflorService
import logging
logging.basicConfig(level=logging.INFO)


logger = logging.getLogger("requerimentos")
router = APIRouter(
    prefix="/requerimentos",
    tags=["REQUERIMENTOS"]
)

@router.post("/repflor/{identificador}")
async def up_requerimentos_repflor(identificador: str):
    try:
        identificador_formatted = identificador+"/INEMA/REPFLOR"
        service = RepflorService().processar(identificador_formatted)
        return service
    except Exception as e:
        print(f"Erro ao atualizar repflors: {e}")
        return {"error": str(e)}
    
@router.get("/repflor-status/{identificador}")
async def consulta_status_repflor(identificador: str):
    try:
        identificador_formatted = identificador+"/INEMA/REPFLOR"
        service = RepflorService().consultar_status(identificador_formatted)
        return service
    except Exception as e:
        print(f"Erro ao consultar status repflor: {e}")
        return {"error": str(e)}