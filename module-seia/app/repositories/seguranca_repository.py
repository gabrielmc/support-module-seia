from typing import List, Optional
from app.core.database import get_db_connection

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
        with get_db_connection(self.desenvolvimento) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                row = cursor.fetchone()
                if row:
                    return {
                        "ide_pessoa_fisica": row[0],
                        "ide_perfil": row[1]
                    }
        return None

    def gerar_script_update(
        self,
        ide_pessoa_fisica: int,
        novo_perfil: int
    ):
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
        with get_db_connection(self.homologacao) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.rowcount