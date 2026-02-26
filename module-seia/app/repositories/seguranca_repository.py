import logging
from typing import Optional
from app.core.database import get_db_connection

logger = logging.getLogger("executar_scripts_transacional")

class SegurancaRepository:
    
    desenvolvimento = "DSV"
    homologacao = "HML"
    
    def buscar_por_nome_usuario(self, nome_usuario: str) -> Optional[dict]:
        sql = """
            SELECT
                pf.ide_pessoa_fisica,
                u.ide_perfil
            FROM pessoa_fisica pf
            JOIN usuario u ON u.ide_pessoa_fisica = pf.ide_pessoa_fis
            WHERE pf.nom_pessoa ILIKE %(nome_usuario)s
        """
        params = {"nome_usuario": nome_usuario}
        with get_db_connection([self.desenvolvimento]) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                row = cursor.fetchone()
                if row:
                    return {
                        "ide_pessoa_fisica": row[0],
                        "ide_perfil": row[1]
                    }
        return None

    def gerar_script_update(self, ide_pessoa_fisica: int, novo_perfil: int):
        params = {}
        if ide_pessoa_fisica:
            params["ide_pessoa_fisica"] = ide_pessoa_fisica
            params["novo_perfil"] = novo_perfil
            sql = f"""
                UPDATE usuario u
                    SET ide_perfil = %(novo_perfil)s
                WHERE u.ide_pessoa_fisica = %(ide_pessoa_fisica)s
            """
            with get_db_connection(self.homologacao) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    return cursor.rowcount
    
    def atualizar_status_dsv_hml(self, ide_pessoa_fisica: int, novo_status: int):
        params = {
            "ide_pessoa_fisica": ide_pessoa_fisica,
            "novo_status": novo_status
        }
        sql = f"""
            UPDATE usuario u
                SET ide_status_usuario = %(novo_status)s
            WHERE u.ide_pessoa_fisica = %(ide_pessoa_fisica)s
        """
        with get_db_connection(self.desenvolvimento) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.rowcount
    
    def atualizar_email_e_perfil(self, cpf: str, email: str):
        query_busca = """
            SELECT P.IDE_PESSOA
            FROM PESSOA P
            WHERE P.IDE_PESSOA IN (
                SELECT PF.IDE_PESSOA_FISICA
                FROM PESSOA_FISICA PF
                WHERE PF.NUM_CPF = %(cpf)s
            )
            LIMIT 1;
        """

        query_update_email = """
            UPDATE pessoa
            SET des_email = %(email)s
            WHERE ide_pessoa = %(ide_pessoa)s;
        """

        query_update_perfil = """
            UPDATE usuario
            SET ide_perfil = 2
            WHERE ide_pessoa_fisica = %(ide_pessoa)s;
        """

        with get_db_connection(self.desenvolvimento) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query_busca, {"cpf": cpf})
                row = cursor.fetchone()
                if not row:
                    return {
                        "sucesso": False,
                        "mensagem": "CPF não encontrado."
                    }

                ide_pessoa = row[0]
                # Atualiza email
                cursor.execute(query_update_email, {
                    "email": email,
                    "ide_pessoa": ide_pessoa
                })

                # Atualiza perfil
                cursor.execute(query_update_perfil, {
                    "ide_pessoa": ide_pessoa
                })

                return {
                    "sucesso": True,
                    "ide_pessoa": ide_pessoa,
                    "mensagem": "Email e perfil atualizados com sucesso."
                }

    def buscar_pessoa_por_cpf(self, cpf: str):
        query = """
            SELECT P.IDE_PESSOA
            FROM PESSOA P
            WHERE P.IDE_PESSOA IN (
                SELECT PF.IDE_PESSOA_FISICA
                FROM PESSOA_FISICA PF
                WHERE PF.NUM_CPF = %(cpf)s
            )
            LIMIT 1;
        """
        with get_db_connection(self.desenvolvimento) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"cpf": cpf})
                row = cursor.fetchone()
        return row[0] if row else None
    
    def executar_scripts_transacional(self, scripts: list[dict]):
        total_statements = 0
        total_linhas_afetadas = 0
        try:
            with get_db_connection(self.desenvolvimento) as connection:
                with connection.cursor() as cursor:
                    for index_script, script_obj in enumerate(scripts):
                        nome_arquivo = script_obj["nome_arquivo"]
                        conteudo = script_obj["conteudo"]
                        statements = [
                            s.strip()
                            for s in conteudo.split(";")
                            if s.strip()
                        ]
                        for index_stmt, statement in enumerate(statements):
                            try:
                                cursor.execute(statement)
                                total_statements += 1
                                if cursor.rowcount != -1:
                                    total_linhas_afetadas += cursor.rowcount
                            except Exception as db_error:
                                connection.rollback()
                                logger.error(
                                    f"Erro no arquivo {nome_arquivo} | "
                                    f"Statement {index_stmt + 1} | "
                                    f"{str(db_error)}",
                                    exc_info=True
                                )
                                return {
                                    "sucesso": False,
                                    "erro_sql": str(db_error).strip(),
                                    "arquivo_com_erro": nome_arquivo,
                                    "statement_index": index_stmt + 1,
                                    "statement_falhou": statement[:500]
                                }
                    connection.commit()
            return {
                "sucesso": True,
                "statements_executados": total_statements,
                "linhas_afetadas": total_linhas_afetadas
            }
        except Exception as e:
            logger.error(f"Erro inesperado na execução: {str(e)}", exc_info=True)
            return {
                "sucesso": False,
                "erro_inesperado": str(e)
            }
