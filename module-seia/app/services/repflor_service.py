import logging
from app.repositories.repflor_repository import RepflorRepository

logger = logging.getLogger("repflor_service")

class RepflorService:
    
    def __init__(self):
        self.repository = RepflorRepository()
    
    def consultar_status(self, identificador: str):
        try:
            resultado = self.repository.buscar_por_identificador(identificador)
            if not resultado:
                return {"mensagem": "Não encontrado"}
            if resultado["ide_status_requerimento"] != 5:
                return {"mensagem": "Status não permite atualização"}
            return {
                "sucesso": True,
                "id_requerimento": resultado["id_requerimento"],
                "ide_status_requerimento": resultado["ide_status_requerimento"]
            }
        except Exception as e:
            logger.error(f"Erro em consultar_status: {str(e)}", exc_info=True)
            return {
                "sucesso": False,
                "mensagem": "Ocorreu um erro ao consultar o status do requerimento."
            }
    
    def processar(self, identificador: str):
        try:
            resultado = self.repository.buscar_por_identificador(identificador)
            if not resultado:
                return {"mensagem": "Não encontrado"}
            if resultado["ide_status_requerimento"] != 5:
                return {"mensagem": "Status não permite atualização"}

            processo_formado = 8 # Status "Processo Formador"
            rows_dsv, rows_hml, script_text = self.repository.gerar_script_update(
                resultado["id_requerimento"],
                novo_status = processo_formado
            )
            if rows_dsv == 0 or rows_hml == 0:
                return {
                    "sucesso": False,
                    "mensagem": "Falha ao atualizar os status nos ambientes"
                }
            return {
                "sucesso": True,
                "ambiente": "DSV → HML",
                "linhas_dsv": rows_dsv,
                "linhas_hml": rows_hml,
                "script": script_text
            }
        except Exception as e:
            logger.error(f"Erro em processar: {str(e)}", exc_info=True)
            return {
                "sucesso": False,
                "mensagem": "Ocorreu um erro ao processar o requerimento."
            }
