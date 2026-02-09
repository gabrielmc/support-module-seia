from app.repositories.relatorio_repository import RelatorioRepository

class RelatorioService:
    
    def __init__(self):
        self.repository = RelatorioRepository()
    
    def relatorio_uc(self, periodo: str):
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