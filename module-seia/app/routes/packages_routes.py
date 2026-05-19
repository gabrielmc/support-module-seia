# app/routes/packages_routes.py

import logging
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.seguranca_service import SegurancaService
from app.core.dependencies import CommonAuth


router = APIRouter(
    prefix="/pacotes",
    tags=["PACOTE"]
)
logger = logging.getLogger("pacotes")

@router.post("/executar-scripts-zip")
async def executar_scripts_zip(file: UploadFile = File(...), auth: bool = CommonAuth):
    logger.info(f"POST /executar-scripts-zip")
    try:
        print(f"Usuário logado: {auth.username}")
        if not file.filename.endswith(".zip"):
            raise HTTPException(status_code=400, detail="Arquivo deve ser .zip")
        resultado = await SegurancaService().processar_zip_e_executar(file)
        return resultado
    except Exception as e:
        logger.warning(f"EXCEPTION - POST - /executar-scripts-zip erro : {e}")
        return {"sucesso": False, "error": str(e)}

@router.post("/validar-imagem")
async def validar_imagem(file: UploadFile = File(...), auth: bool = CommonAuth):
    logger.info("POST /validar-imagem")
    try:
        print(f"Usuário logado: {auth.username}")
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