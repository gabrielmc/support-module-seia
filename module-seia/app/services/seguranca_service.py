import os, io, zipfile
import logging
from fastapi import HTTPException
from datetime import datetime
from app.repositories.seguranca_repository import SegurancaRepository

logger = logging.getLogger("script_zip_execution")

class SegurancaService:
    
    def __init__(self):
        self.repository = SegurancaRepository()
        self.diretorio_saida = "/home/gmuniz/Documentos/artefatos-seia/tickets-SEIA/login-branco/"
    
    def atualizar_perfil(self, nome_usuario: str, novo_perfil: int):
        try:
            resultado = self.repository.buscar_por_nome_usuario(nome_usuario)
            if not resultado:
                return {"mensagem": "Não encontrado"}

            rows_dsv, rows_hml, script_text = self.repository.gerar_script_update(
                resultado["ide_pessoa_fisica"],
                novo_perfil = novo_perfil
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
            logger.error(f"Erro em atualizar_perfil: {str(e)}", exc_info=True)
            return {
                "sucesso": False,
                "mensagem": "Ocorreu um erro ao atualizar o perfil do usuário."
            }
    
    def incluir_email_usuario(self, usuarios: list):
        try:
            resultados = []
            for usuario in usuarios:
                cpf_limpo = ''.join(filter(str.isdigit, usuario.cpf))
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
        except Exception as e:
            logger.error(f"Erro em incluir_email_usuario: {str(e)}", exc_info=True)
            return {
                "sucesso": False,
                "mensagem": "Ocorreu um erro ao atualizar os usuários."
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

    async def processar_zip_e_executar(self, file):
        contents = await file.read()
        total_arquivos = 0
        try:
            with zipfile.ZipFile(io.BytesIO(contents)) as z:
                # Apenas arquivos .sql
                sql_files = sorted(
                    [f for f in z.namelist() if f.endswith(".sql")]
                )
                if not sql_files:
                    raise HTTPException(
                        status_code=400,
                        detail="Nenhum arquivo .sql encontrado no zip"
                    )
                scripts = []
                for filename in sql_files:
                    total_arquivos += 1
                    with z.open(filename) as f:
                        sql_content = f.read().decode("utf-8")
                        self._validar_sql(sql_content)
                        scripts.append({
                            "nome_arquivo": filename,
                            "conteudo": sql_content
                        })

                # Executa tudo dentro de uma transação
                resultado = self.repository.executar_scripts_transacional(scripts)
                # 🔴 Se houve erro SQL controlado
                if not resultado.get("sucesso"):
                    logger.warning(
                        f"Erro controlado na execução do pacote: {resultado}"
                    )
                    return {
                        "sucesso": False,
                        "arquivos_processados": total_arquivos,
                        **resultado
                    }

                # ✅ Se executou com sucesso
                logger.info(
                    f"Execução finalizada | Arquivos: {total_arquivos} | "
                    f"Statements: {resultado['statements_executados']} | "
                    f"Linhas afetadas: {resultado['linhas_afetadas']}"
                )
                return {
                    "sucesso": True,
                    "arquivos_processados": total_arquivos,
                    "statements_executados": resultado["statements_executados"],
                    "linhas_afetadas": resultado["linhas_afetadas"]
                }
        except Exception as e:
            logger.error(
                f"Erro inesperado ao executar scripts do zip: {str(e)}",
                exc_info=True
            )
            return {
                "sucesso": False,
                "erro_inesperado": "Erro interno inesperado ao processar o pacote."
            }

    def _validar_sql(self, sql: str):
        sql_upper = sql.upper()
        comandos_proibidos = [
            "DROP DATABASE",
            "ALTER SYSTEM",
            "TRUNCATE DATABASE",
            "DELETE ",
            "DROP TABLE"
        ]
        for comando in comandos_proibidos:
            if comando in sql_upper:
                raise HTTPException(
                    status_code=400,
                    detail=f"Comando proibido detectado: {comando}"
                )
