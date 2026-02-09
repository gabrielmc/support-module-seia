from typing import List, Optional
from app.core.database import get_db_connection


class ConsultaRepository:
    
    desenvolvimento = "DSV"
    homologacao = "HML"

    def buscar_datas_boletos(self, numeros_boletos: List[str]) -> dict:
        sql = """
            SELECT
                bpr.num_boleto,
                bpr.dtc_pagamento,
                bpr.dtc_vencimento
            FROM boleto_pagamento_requerimento bpr
            WHERE bpr.num_boleto = ANY(%s);
        """
        resultado = {}
        with get_db_connection(self.desenvolvimento) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (numeros_boletos,))
                for num_boleto, dtc_pagamento, dtc_vencimento in cursor.fetchall():
                    resultado[num_boleto] = {
                        "dtc_pagamento": (
                            dtc_pagamento.strftime("%d/%m/%Y")
                            if dtc_pagamento else None
                        ),
                        "dtc_vencimento": (
                            dtc_vencimento.strftime("%d/%m/%Y")
                            if dtc_vencimento else None
                        )
                    }
        return resultado

    def buscar_boletos(self, numero_boleto: Optional[str], datas_pagamento: Optional[List[str]]):
        filtros = []
        params = {}
        if numero_boleto:
            filtros.append("bpr.num_boleto = %(numero_boleto)s")
            params["numero_boleto"] = numero_boleto
        if datas_pagamento:
            filtros.append("bpr.dtc_pagamento::date = ANY(%(datas_pagamento)s)")
            params["datas_pagamento"] = datas_pagamento
        where_clause = " AND ".join(filtros) if filtros else "1=1"
        sql = f"""
            SELECT
                bpr.num_boleto,
                bpr.dtc_pagamento,
                bpr.dtc_vencimento
            FROM boleto_pagamento_requerimento bpr
            WHERE {where_clause};
        """
        with get_db_connection(self.desenvolvimento) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()