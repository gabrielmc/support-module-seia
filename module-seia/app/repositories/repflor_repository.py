import logging
from app.core.database.conn_base import get_db_connection

logger = logging.getLogger("repflor_repository")

class RepflorRepository:

    desenvolvimento = "DSV"
    homologacao = "HML"

    def buscar_por_identificador(self, identificador: str) -> dict | None:
        connection = None
        cursor = None
        try:
            identificador = identificador.strip()
            sql = """
            SELECT * FROM tramitacao_requerimento trq
            WHERE trq.ide_requerimento in (
                SELECT rq.ide_requerimento FROM requerimento rq
                WHERE rq.num_requerimento LIKE %(identificador)s
            )
            --AND trq.ide_status_requerimento = 5
            ORDER BY trq.dtc_movimentacao DESC
            LIMIT 1;
            """
            with get_db_connection(self.desenvolvimento) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        sql,
                        {"identificador": f"%{identificador}%"}
                    )
                    row = cursor.fetchone()

            if not row:
                return None
            return {
                "id_requerimento": row[0],
                "ide_status_requerimento": row[1]
            }
        except Exception as e:
            logger.error(f"Erro em buscar_por_identificador: {str(e)}", exc_info=True)
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def atualizar_status_em_ambiente(self, ambiente: str, id_requerimento: int, novo_status: int) -> int:
        connection = None
        cursor = None
        try:
            sql = """
                UPDATE tramitacao_requerimento
                SET ide_status_requerimento = %(novo_status)s
                WHERE ide_tramitacao_requerimento = %(id_requerimento)s;
            """
            with get_db_connection(ambiente) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        sql,
                        {
                            "id_requerimento": id_requerimento,
                            "novo_status": novo_status
                        }
                    )
                    rows = cursor.rowcount
                if rows == 0:
                    conn.rollback()
                else:
                    conn.commit()
            return rows
        except Exception as e:
            logger.error(f"Erro em atualizar_status_em_ambiente: {str(e)}", exc_info=True)
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def atualizar_status_dsv_hml(self, id_requerimento: int, novo_status: int) -> dict:
        rows_dsv = self.atualizar_status_em_ambiente(
            self.desenvolvimento,
            id_requerimento,
            novo_status
        )
        if rows_dsv == 0: return 0

        rows_hml = self.atualizar_status_em_ambiente(
            self.homologacao,
            id_requerimento,
            novo_status
        )
        if rows_hml == 0: return 0

        #rows_hml = 1  #Simula sucesso em HML
        return rows_dsv, rows_hml

    def gerar_script_update(self, id_requerimento: int, novo_status: int) -> str:
        connection = None
        cursor = None
        try:
            rows_dsv, rows_hml = self.atualizar_status_dsv_hml(id_requerimento, novo_status)
            script_text = f"""
                    UPDATE tramitacao_requerimento
                    SET ide_status_requerimento = {novo_status}
                    WHERE ide_tramitacao_requerimento = {id_requerimento};
            """.strip()
            return rows_dsv, rows_hml, script_text
        except Exception as e:
            logger.error(f"Erro em gerar_script_update: {str(e)}", exc_info=True)
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
