from typing import List, Optional
from app.core.database import get_db_connection


class ProcessoRepository:
    
    desenvolvimento = "DSV"
    homologacao = "HML"

    def Removendo_status_anterior(self, tramitacao: Optional[str] = None):
        query = """
            UPDATE controle_tramitacao ct
            SET
                ind_fim_da_fila = false
            WHERE
                ct.ide_controle_tramitacao = %(tramitacao)s
        """
        if tramitacao:
            with get_db_connection(self.desenvolvimento) as conn:
                with conn.cursor() as cursor:
                        cursor.execute(
                            query,
                            {"tramitacao": f"%{tramitacao}%"}
                        )
                        row = cursor.fetchone()
            if not row:
                return None
            return {
                "tramitacao": row[0],
                "status": row[1]
            }
