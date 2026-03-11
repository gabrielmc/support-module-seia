from app.core.config import settings
from app.repositories.consulta_repository import ConsultaRepository


class MonitoramentoService:

    # ==========================
    # Monitoramento de ambientes
    # ==========================
    @staticmethod
    def monitorar_memoria_jboss():
        try:
            ambientes = {
                "memoria_dsv": settings.JBOSS_URL_DSV,
                "memoria_hml": settings.JBOSS_URL_HML,
                "memoria_treinamento": settings.JBOSS_URL_TREINAMENTO
            }
            return {
                chave: ConsultaRepository().monitorar_memoria_jboss(url)
                for chave, url in ambientes.items()
            }
        except Exception as e:
            print(f"Erro ao monitorar status de requerimentos: {e}")
    
    @staticmethod
    def monitorar_atualizacao_banco():
        try:
            return ConsultaRepository().monitorar_atualizacao_banco()
        except Exception as e:
            print(f"Erro ao monitorar status de requerimentos: {e}")
