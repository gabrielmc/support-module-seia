from fastapi import FastAPI
from app.core.config import settings
from app.routes.cefit_routes import router as cemit_router
from app.routes.processo_routes import router as processo_router
from app.routes.requerimentos_routes import router as requerimentos_router
from app.routes.seguranca_routes import router as seguranca_router
from app.routes.relatorios_routes import router as relatorios_router


app = FastAPI(
    title="Module-SEIA",
    description="API do Module-SEIA baseada em informações ambientais, florestais e biomas",
    version="1.0.0"
)

app.include_router(cemit_router)
app.include_router(processo_router)
app.include_router(requerimentos_router)
app.include_router(seguranca_router)
app.include_router(relatorios_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True
    )