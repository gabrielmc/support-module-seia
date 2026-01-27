from fastapi import FastAPI

#from app.routes.processo_routes import router as processo_router
#from app.routes.seguranca_routes import router as seguranca_router
#from app.routes.relatorios_routes import router as relatorios_router
from app.routes.requerimentos_routes import router as requerimentos_router
from app.routes.consulta_routes import router as consultas_router


app = FastAPI(
    title="Module-SEIA",
    description="API do Module-SEIA baseada em informações ambientais, florestais e biomas",
    version="1.0.0"
)

#app.include_router(processo_router)
#app.include_router(seguranca_router)
#app.include_router(relatorios_router)
app.include_router(requerimentos_router)
app.include_router(consultas_router)