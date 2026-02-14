# app/routes/consultas_routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List, Optional
from app.services.consulta_service import ConsultaService
from app.models.schemas.retorno_cnab_schema import RetornoArquivoSchema
import logging
logging.basicConfig(level=logging.INFO)


logger = logging.getLogger("consultas")
router = APIRouter(
    prefix="/consultas",
    tags=["CONSULTAS"]
)

@router.post("/registrar-retorno", response_model=RetornoArquivoSchema)
async def registrar_retorno(arquivo: UploadFile = File(...)):
    try:
        if not arquivo.filename.endswith(".txt"):
            raise HTTPException(
                status_code=400,
                detail="Arquivo inválido. Envie um arquivo .txt"
            )
        conteudo = await arquivo.read()
        linhas = conteudo.decode("utf-8").splitlines()
        boletos_processados = ConsultaService.processar_retorno_cnab(linhas)
        return {
            "arquivo": arquivo.filename,
            "total_processados": len(boletos_processados),
            "boletos": boletos_processados
        }
    except Exception as e:
        logger.info(f"POST/registrar-retorno - {e}")
        print(f"Erro ao excluir requerimento logicamente: {e}")
        raise e

@router.get("/boletos")
async def consultar_boletos(
        numero_boleto: Optional[str] = Query(None, description="Número do boleto"),
        datas_pagamento: Optional[List[str]] = Query(None, description="Lista de datas de pagamento (YYYY-MM-DD)")
    ):
    try:
        #Consulta boletos por número, data de pagamento ou ambos.
        return {
            "filtros": {
                "numero_boleto": numero_boleto,
                "datas_pagamento": datas_pagamento
            },
            "resultado": ConsultaService.consultar_boletos(
                numero_boleto,
                datas_pagamento
            )
        }
    except Exception as e:
        logger.info(f"GET/boletos - {e}")
        print(f"Erro ao excluir requerimento logicamente: {e}")
        raise e