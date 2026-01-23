# app/routes/processo_routes.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/processos",
    tags=["PROCESSO"]
)

@router.get("/")
def listar_processos():
    return {"modulo": "PROCESSO"}
