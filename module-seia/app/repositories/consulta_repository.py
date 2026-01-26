from typing import List, Optional
from app.core.database import get_db_connection


class ConsultaRepository:

    @staticmethod
    def buscar_boletos(
        numero_boleto: Optional[str] = None,
        datas_pagamento: Optional[List[str]] = None
    ):
        query = """
            SELECT
                b.num_boleto,
                b.ide_requerimento,
                b.dtc_emissao   AS data_emissao,
                b.dtc_pagamento AS data_pagamento,
                b.dtc_vencimento AS data_vencimento
            FROM boleto_pagamento_requerimento b
            WHERE 1 = 1
        """

        params = []
        if numero_boleto:
            query += " AND b.num_boleto = %s"
            params.append(numero_boleto)

        if datas_pagamento:
            query += " AND b.dtc_pagamento = ANY(%s)"
            params.append(datas_pagamento)

        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                colunas = [desc[0] for desc in cursor.description]
                resultados = cursor.fetchall()

        return [dict(zip(colunas, row)) for row in resultados]
