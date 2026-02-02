from fastapi import FastAPI
from app.routes.requerimentos_routes import router as requerimentos_router
from app.routes.consulta_routes import router as consulta_router

app = FastAPI(
    title="Module-SEIA",
    description="API do Module-SEIA baseada em informações ambientais, florestais e biomas",
    version="1.0.0"
)

app.include_router(requerimentos_router)
app.include_router(consulta_router)