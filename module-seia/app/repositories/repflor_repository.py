from app.core.database import get_db_connection

class RepflorRepository:

    def buscar_por_identificador(self, identificador: str) -> dict | None:
        try:
            identificador = identificador.strip()
            desenvolvimento = "DSV"
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
            with get_db_connection(desenvolvimento) as conn:
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
        
    def _atualizar_status_em_ambiente(self, ambiente: str, id_requerimento: int, novo_status: int) -> int:
        """
        Executa o update em um ambiente específico (DSV ou HML)
        Retorna quantidade de linhas afetadas
        """
        sql = """
            UPDATE tramitacao_requerimento
            SET ide_status_requerimento = %(novo_status)s
            WHERE id_tramitacao_requerimento = %(id_requerimento)s;
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
    
    def atualizar_status_dsv_hml(self, id_requerimento: int, novo_status: int) -> dict:
        #Atualiza primeiro em DSV e, se tiver sucesso, replica em HML
        desenvolvimento = "DSV"
        homologacao = "HML"
        rows_dsv = self._atualizar_status_em_ambiente(
            desenvolvimento,
            id_requerimento,
            novo_status
        )
        if rows_dsv == 0: return 0

        rows_hml = self._atualizar_status_em_ambiente(
            homologacao,
            id_requerimento,
            novo_status
        )
        if rows_hml == 0: return 0

        return rows_dsv, rows_hml

    def gerar_script_update(self, id_requerimento: int, novo_status: int) -> str:
        rows_dsv, rows_hml = self.atualizar_status_dsv_hml(id_requerimento, novo_status)
        script_text = f"""
            BEGIN;
                UPDATE tramitacao_requerimento
                SET ide_status_requerimento = {novo_status}
                WHERE id_tramitacao_requerimento = {id_requerimento};
            COMMIT;
        """.strip()
        return rows_dsv, rows_hml, script_text