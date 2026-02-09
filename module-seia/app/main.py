from fastapi import FastAPI
from app.routes.requerimentos_routes import router as requerimentos_router
from app.routes.consultas_routes import router as consultas_router
from app.routes.relatorios_routes import router as relatorios_router

app = FastAPI(
    title="Module-SEIA",
    description="API do Module-SEIA baseada em informações ambientais, florestais e biomas",
    version="1.0.0"
)

app.include_router(requerimentos_router)
app.include_router(consultas_router)
app.include_router(relatorios_router)