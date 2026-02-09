from app.repositories.seguranca_repository import SegurancaRepository

class SegurancaService:
    
    def __init__(self):
        self.repository = SegurancaRepository()
    
    def atualizar_perfil(self, nome_usuario: str):
        resultado = self.repository.buscar_por_nome_usuario(nome_usuario)
        if not resultado:
            return {"mensagem": "Não encontrado"}

        perfil_diretor = 9 # Perfil Diretor - mudança realizada com o perfil mais recorrente 
        rows_dsv, rows_hml, script_text = self.repository.gerar_script_update(
            resultado["ide_pessoa_fisica"],
            novo_perfil = perfil_diretor
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