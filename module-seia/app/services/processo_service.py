from typing import List, Optional
from app.repositories.processo_repository import ProcessoRepository


class ProcessoService:

    """
    Ajustando status da tabela de controle_tramitacao
    """
    @staticmethod
    def removendo_status_anterior(tramitacao: Optional[str] = None):
        try:
            return ProcessoRepository().removendo_status_anterior(tramitacao=tramitacao)
        except Exception as e:
            print(f"Erro ao remover status anterior: {e}")
            raise e