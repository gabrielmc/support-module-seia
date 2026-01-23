from app.core.database import get_db_connection

class RepflorRepository:

    def buscar_por_identificador(self, identificador: str) -> dict | None:
        try:
            identificador = identificador.strip()
            sql = """
            SELECT * FROM tramitacao_requerimento trq
            WHERE trq.ide_requerimento in ( 
                SELECT rq.ide_requerimento FROM requerimento rq
                WHERE rq.num_requerimento like '%(identificador)s'
            )
            AND trq.ide_status_requerimento = 5
            ORDER BY trq.dtc_movimentacao DESC
            LIMIT 1;
            """
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, {"identificador": identificador})
                    row = cursor.fetchone()

            if not row:
                return None

            return {
                "id_requerimento": row[0],
                "ide_status_requerimento": row[1]
            }
        except Exception as e:
            raise e

    def atualizar_status(self, id_requerimento: int, novo_status: int) -> int:
        try:
            sql = """
            BEGIN;
                UPDATE tramitacao_requerimento
                SET ide_status_requerimento = %(novo_status)s
                WHERE id_tramitacao_requerimento = %(id_requerimento)s;
            COMMIT;
            """

            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        sql,
                        {
                            "id_requerimento": id_requerimento,
                            "novo_status": novo_status
                        }
                )
                return cursor.rowcount
        except Exception as e:
            raise e

    def gerar_script_update(self, id_requerimento: int, novo_status: int) -> str:
        #self.atualizar_status(id_requerimento, novo_status)
        return f"""
            BEGIN;
                UPDATE tramitacao_requerimento
                SET ide_status_requerimento = {novo_status}
                WHERE id_tramitacao_requerimento = {id_requerimento};
            COMMIT;
        """.strip()
