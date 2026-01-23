# app/routes/seguranca_routes.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/seguranca",
    tags=["SEGURANÇA"]
)

@router.get("/health")
def health_check():
    return {"status": "segurança OK"}
