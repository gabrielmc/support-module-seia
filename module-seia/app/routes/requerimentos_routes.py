# app/routes/requerimentos_routes.py
from fastapi import APIRouter
from app.models.schemas.repflor_schema import RepflorRequest, RepflorResponse
from app.services.repflor_service import RepflorService

router = APIRouter(
    prefix="/requerimentos",
    tags=["REQUERIMENTOS"]
)

@router.post(
    "/repflor",
    response_model=RepflorResponse
)
def up_requerimentos_repflor(payload: RepflorRequest):
    try:
        service = RepflorService().processar(payload)
        return service
    except Exception as e:
        return {"error": str(e)}
    
@router.get(
    "/repflor-consulta-status/{identificador}",
)
def up_requerimentos_repflor(identificador: str):
    try:
        service = RepflorService().consultar_status(identificador)
        return service
    except Exception as e:
        return {"error": str(e)}