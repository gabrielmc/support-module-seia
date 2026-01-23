from app.repositories.repflor_repository import RepflorRepository
from app.models.schemas.repflor_schema import RepflorRequest, RepflorResponse


class RepflorService:
    
    def __init__(self):
        self.repository = RepflorRepository()

    def processar(self, identificador: str): # 2025.001.005254/INEMA/REPFLOR
        resultado = self.repository.buscar_por_identificador(identificador)
        
        if not resultado:
            return {"mensagem": "Não encontrado"}
        if resultado["ide_status_requerimento"] != 5:
            return {"mensagem": "Status não permite atualização"}

        processo_formado = 8 # Status "Processo Formador"
        script = self.repository.gerar_script_update(
            resultado["id_requerimento"],
            novo_status = processo_formado
        )
        return {
            "mensagem": "Update permitido, JÁ EXECUTADO EM -> [DESENVOLVIMENTO].",
            "script": script
        }