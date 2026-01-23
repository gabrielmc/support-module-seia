# app/routes/cefit_routes.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/cefit",
    tags=["CEFIT"]
)

@router.get("/")
def listar_cefit():
    return {"modulo": "CEFIT"}
