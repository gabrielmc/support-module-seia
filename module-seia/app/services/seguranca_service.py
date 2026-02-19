import os
from datetime import datetime
from app.repositories.seguranca_repository import SegurancaRepository

class SegurancaService:
    
    def __init__(self):
        self.repository = SegurancaRepository()
        self.diretorio_saida = "/home/gmuniz/Documentos/artefatos-seia/tickets-SEIA/login-branco/"
    
    def atualizar_perfil(self, nome_usuario: str):
        resultado = self.repository.buscar_por_nome_usuario(nome_usuario)
        if not resultado:
            return {"mensagem": "Não encontrado"}

        perfil_diretor = 9 # Perfil Diretor
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
    
    def incluir_email_usuario(self, usuarios: list):
        resultados = []
        print(f"Processando inclusão de email para {len(usuarios)} usuários...")
        for usuario in usuarios:
            cpf_limpo = ''.join(filter(str.isdigit, usuario.cpf))
            print(f"Processando CPF: {cpf_limpo} com email: {usuario.email}")
            atualizado = self.repository.atualizar_email_e_perfil(
                cpf=cpf_limpo,
                email=usuario.email
            )
            resultados.append({
                "cpf": cpf_limpo,
                "email": usuario.email,
                "atualizado": atualizado
            })
        return {
            "sucesso": True,
            "total_processados": len(resultados),
            "detalhes": resultados
        }
        
    def gerar_script_email_por_cpf(self, usuarios: list):
        os.makedirs(self.diretorio_saida, exist_ok=True)
        script_final = ""
        for index, usuario in enumerate(usuarios, start=1):
            cpf_limpo = ''.join(filter(str.isdigit, usuario.cpf))
            ide_pessoa = self.repository.buscar_pessoa_por_cpf(cpf_limpo)
            
            if not ide_pessoa:
                continue  # ignora CPF não encontrado
            email_seguro = usuario.email.replace("'", "''")
            bloco = f"""
                --------------------------------------------ticket - #{usuario.ticket}
                update
                    pessoa
                set
                    des_email = '{email_seguro}'
                where
                    ide_pessoa = {ide_pessoa};

                update
                    usuario
                set
                    ide_perfil = 2
                where
                    ide_pessoa_fisica = {ide_pessoa};

                """
            script_final += bloco

        file_path = os.path.join(
            self.diretorio_saida,
            f"script_email_{datetime.now().strftime('%d%m%Y')}.sql"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(script_final)

        return file_path
