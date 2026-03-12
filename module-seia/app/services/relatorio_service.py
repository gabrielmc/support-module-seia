import logging
from app.repositories.relatorio_repository import RelatoriosRepository

logger = logging.getLogger("relatorio_service")

class RelatorioService:

    def __init__(self):
        self.repository = RelatoriosRepository()

    def relatorio_uc(self, periodo: str):
        try:
            resultado = self.repository.busca_zoneamento_uc(periodo)
            if not resultado or not resultado.get("dados"):
                return {
                    "sucesso": False,
                    "mensagem": "Não encontrado",
                    "ambiente": "HML"
                }
            return {
                "sucesso": True,
                "ambiente": "HML",
                "colunas": resultado["colunas"],
                "dados": resultado["dados"]
            }
        except Exception as e:
            logger.error(f"Erro em relatorio_uc: {str(e)}", exc_info=True)
            return {
                "sucesso": False,
                "mensagem": "Ocorreu um erro ao gerar o relatório.",
                "ambiente": "HML"
            }
