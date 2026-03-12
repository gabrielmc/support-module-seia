import logging
from typing import Optional
from app.repositories.processo_repository import ProcessoRepository

logger = logging.getLogger("processo_service")

class ProcessoService:

    @staticmethod
    def removendo_status_anterior(tramitacao: Optional[str] = None):
        try:
            return ProcessoRepository().removendo_status_anterior(tramitacao=tramitacao)
        except Exception as e:
            logger.error(f"Erro em removendo_status_anterior: {str(e)}", exc_info=True)
            return None
    
    @staticmethod 
    def excluir_requerimento_logicamente(requerente: str, cpf_cnpj: str, imovel: str):
        try:
            resultado = ProcessoRepository().buscar_requerimento_por_dados(
                requerente=requerente,
                cpf_cnpj=cpf_cnpj,
                imovel=imovel
            )
            if not resultado:
                return {
                    "sucesso": False,
                    "mensagem": "Nenhum requerimento encontrado"
                }
            ide_requerimento = resultado["ide_requerimento"]
            ide_requerimento_imovel = resultado["ide_requerimento_imovel"]
            if not ide_requerimento or not ide_requerimento_imovel:
                return {
                    "sucesso": False,
                    "mensagem": "IDs inválidos para exclusão."
                }
            # Executa updates
            ProcessoRepository().excluir_requerimento(ide_requerimento)
            ProcessoRepository().excluir_requerimento_imovel(ide_requerimento_imovel)
            return {
                "sucesso": True,
                "ide_requerimento": ide_requerimento,
                "ide_requerimento_imovel": ide_requerimento_imovel,
                "mensagem": "Requerimento excluído logicamente com sucesso"
            }
        except Exception as e:
            logger.error(f"Erro em excluir_requerimento_imovel: {str(e)}", exc_info=True)
            return {
                "sucesso": False,
                "mensagem": "Ocorreu um erro ao tentar excluir o requerimento."
            }
