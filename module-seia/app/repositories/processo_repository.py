from typing import Optional
from app.core.database import get_db_connection


class ProcessoRepository:
    
    desenvolvimento = "DSV"
    homologacao = "HML"

    #Ajustando status da tabela de controle_tramitacao
    def removendo_status_anterior(self, tramitacao: Optional[str] = None):
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
    
    def buscar_requerimento_por_dados(self, requerente: str, cpf_cnpj: str, imovel: str):
        query = """
            SELECT R.IDE_REQUERIMENTO_IMOVEL, R.IDE_REQUERIMENTO
                FROM REQUERIMENTO_IMOVEL R
            WHERE R.IDE_IMOVEL IN (
                SELECT IR.IDE_IMOVEL_RURAL
                    FROM IMOVEL_RURAL IR
                WHERE IR.IDE_IMOVEL_RURAL IN (
                    SELECT T.IDE_IMOVEL
                        FROM PESSOA_IMOVEL T
                    WHERE T.IDE_PESSOA = (
                        SELECT PF.IDE_PESSOA_FISICA
                            FROM PESSOA_FISICA PF
                        WHERE PF.NOM_PESSOA ILIKE %(requerente)s
                        AND PF.NUM_CPF ILIKE %(cpf_cnpj)s
                    )
                )
                AND IR.DES_DENOMINACAO ILIKE %(imovel)s
            )
            LIMIT 1;
        """
        with get_db_connection(self.desenvolvimento) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    {
                        "requerente": f"%{requerente}%",
                        "cpf_cnpj": f"%{cpf_cnpj}%",
                        "imovel": f"%{imovel}%"
                    }
                )
                row = cursor.fetchone()
        if not row:
            return None
        return {
            "ide_requerimento_imovel": row[0],
            "ide_requerimento": row[1]
        }
    
    # Update requerimento
    def excluir_requerimento(self, ide_requerimento: int):
        query = """
            UPDATE requerimento
            SET ind_excluido = TRUE,
                dtc_exclusao = now()
            WHERE ide_requerimento = %(ide_requerimento)s;
        """
        with get_db_connection(self.desenvolvimento) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {
                    "ide_requerimento": ide_requerimento
                })

    # Update requerimento_imovel
    def excluir_requerimento_imovel(self, ide_requerimento_imovel: int):
        query = """
            UPDATE requerimento_imovel
            SET ind_excluido = TRUE,
                dtc_exclusao = now()
            WHERE ide_requerimento_imovel = %(ide_requerimento_imovel)s;
        """
        with get_db_connection(self.desenvolvimento) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {
                    "ide_requerimento_imovel": ide_requerimento_imovel
                })
