from fastapi import FastAPI
from app.routes.requerimentos_routes import router as requerimentos_router
from app.routes.consultas_routes import router as consultas_router
from app.routes.relatorios_routes import router as relatorios_router
from app.routes.processos_routes import router as processos_router
from app.routes.segurancas_routes import router as segurancas_router
from app.routes.packages_routes import router as packages_routes
from app.routes.monitoramentos_routes import router as monitoramentos_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# application logging
from app.core.logging import setup_logging
setup_logging()


app = FastAPI(
    title="Module-SEIA",
    description="API do Module-SEIA baseada em informações ambientais, florestais e biomas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS, # Configurado para permitir apenas os domínios especificados no .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(requerimentos_router)
app.include_router(consultas_router)
app.include_router(relatorios_router)
app.include_router(processos_router)
app.include_router(segurancas_router)
app.include_router(packages_routes)
app.include_router(monitoramentos_router)
