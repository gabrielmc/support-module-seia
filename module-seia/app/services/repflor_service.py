from app.repositories.repflor_repository import RepflorRepository
from app.models.schemas.repflor_schema import RepflorRequest, RepflorResponse


class RepflorService:
    
    def __init__(self):
        self.repository = RepflorRepository()
    
    def consultar_status(self, identificador: str):
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
    
    def processar(self, identificador: str): # 2025.001.005254/INEMA/REPFLOR
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