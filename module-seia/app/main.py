from fastapi import FastAPI
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.routes.relatorios_routes import router as relatorios_router
from app.routes.packages_routes import router as packages_routes
from app.routes.monitoramentos_routes import router as monitoramentos_router
from app.routes.autenticacao_routes import router as auth_router
'''
from app.routes.consultas_routes import router as consultas_router
from app.routes.requerimentos_routes import router as requerimentos_router
from app.routes.segurancas_routes import router as segurancas_router
from app.routes.processos_routes import router as processos_router
'''

# application logging
from app.core.logging import setup_logging
setup_logging()


app = FastAPI(
    title="API do Módulo SEIA 🌿",
    description="""
    # API do Módulo SEIA - Versão Aprimorada 🌿

    Esta é a nova versão da API do **Module-SEIA**, focada em fornecer dados ambientais, florestais e sobre biomas brasileiros.

    # Funcionalidades Principais:

    *   **Relatórios Técnicos**: Geração de relatórios consolidados em formatos CSV e JSON.
    *   **Integração Multi-Ambiente**: Conexão transparente com bancos de dados de Desenvolvimento (DSV) e Homologação (HML).

    # Principais Tecnologias:

    *   **Framework**: FastAPI
    *   **Validação de Dados**: Pydantic V2
    *   **Acesso a Dados**: SQLAlchemy Core + AsyncPG
    *   **Servidor ASGI**: Uvicorn
    """,
    version=settings.VERSION,
    # Novos parâmetros adicionados:
    terms_of_service="http://intranet.empresa.com/licencas-seia",
    contact={
        "name": "Equipe de Sustentação SEIA",
        "email": "gabriel.cerqueira@prodeb.ba.gov.br",
    },
    license_info={
        "name": "Licença Interna - Uso Exclusivo",
        "url": "http://intranet.empresa.com/licencas-seia",
    },
    docs_url="/docs", # URL para o Swagger UI (padrão)
    servers=[
        {"url": "http://localhost:9000", "description": "Ambiente de Desenvolvimento Local"}
        #{"url": "https://seia-dsv.empresa.com", "description": "Ambiente de Desenvolvimento (DSV)"},
        #{"url": "https://seia-hml.empresa.com", "description": "Ambiente de Homologação (HML)"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list, # Configurado para permitir apenas os domínios especificados no .env
    allow_origin_regex=settings.allow_origin_regex, # Permite localhost e IPs internos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)


# [ Rotas sem uso/consumo frequente ]
#app.include_router(requerimentos_router)
#app.include_router(consultas_router)
#app.include_router(processos_router)
#app.include_router(segurancas_router)

app.include_router(relatorios_router)
app.include_router(packages_routes)
app.include_router(monitoramentos_router)