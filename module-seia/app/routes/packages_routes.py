# app/routes/packages_routes.py

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.seguranca_service import SegurancaService


router = APIRouter(
    prefix="/pacotes",
    tags=["PACOTE"]
)
logger = logging.getLogger("pacotes")

@router.post("/executar-scripts-zip")
async def executar_scripts_zip(file: UploadFile = File(...)):
    logger.info(f"POST /executar-scripts-zip")
    try:
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser .zip")
        print(f"Recebido arquivo: {file.filename}")
        resultado = await SegurancaService().processar_zip_e_executar(file)
        return resultado
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /executar-scripts-zip erro : {e}")
        return {"sucesso": False, "error": str(e)}


@router.post("/validar-imagem")
async def validar_imagem(file: UploadFile = File(...)):
    logger.info("POST /validar-imagem")
    try:
        if not (file.filename.endswith(".zip") or file.filename.endswith(".war")):
            raise HTTPException(
                status_code=400,
                detail="Arquivo deve ser .zip ou .war"
            )
        resultado = await SegurancaService().validar_pacote_persistence(file)
        return resultado
    except Exception as e:
        logger.warning(f"Erro na validação pacote: {e}")
        return {"sucesso": False, "erro": str(e)}
