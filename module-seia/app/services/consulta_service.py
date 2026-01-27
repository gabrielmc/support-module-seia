from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from app.repositories.consulta_repository import ConsultaRepository


class ConsultaService:

    REJEICOES = {"02", "03", "26", "30"}
    LIQUIDACOES = {"06", "09", "17"}
    STATUS_MAP = {
        "02": "Rejeição",
        "03": "Rejeição",
        "26": "Rejeição",
        "30": "Rejeição",
        "06": "Liquidação / baixa",
        "09": "Liquidação / baixa",
        "17": "Liquidação / baixa",
    }

    @staticmethod
    def parse_valor(valor_str: str) -> Decimal:
        return Decimal(valor_str) / Decimal("100")

    @staticmethod
    def parse_data(data_str: str):
        if data_str.strip("0") == "":
            return None
        return datetime.strptime(data_str, "%d%m%Y").date()

    @classmethod
    def obter_status_formatado(cls, codigo: str) -> str:
        descricao = cls.STATUS_MAP.get(codigo, "Status desconhecido")
        return f"{codigo} - {descricao}"

    @classmethod
    def processar_retorno_cnab(cls, linhas):
        boletos_processados = []
        boleto_atual = None

        for linha in linhas:
            tipo_registro = linha[13]  # REGISTRO T ou REGISTRO U
            if tipo_registro == "T":
                boleto_atual = {
                    "numero_boleto": linha[37:57].strip()
                }
            elif tipo_registro == "U" and boleto_atual:
                status_u = linha[15:17]
                valor_pago = cls.parse_valor(linha[77:92])
                data_pagamento = cls.parse_data(linha[145:153])

                # Rejeição → ignora
                if status_u in cls.REJEICOES:
                    boleto_atual = None
                    continue

                if status_u in cls.LIQUIDACOES and valor_pago > 0:
                    boletos_processados.append({
                        "numero_boleto": boleto_atual["numero_boleto"],
                        "codigo_status": status_u,
                        "status": cls.obter_status_formatado(status_u),
                        "valor_pago": float(valor_pago),
                        "data_pagamento": (
                            data_pagamento.strftime("%d/%m/%Y")
                            if data_pagamento else None
                        ),
                        "origem": "REGISTRO U"
                    })
                boleto_atual = None
        return boletos_processados

    @staticmethod
    def consultar_boletos(numero_boleto: Optional[str], datas_pagamento: Optional[List[str]]):
        return ConsultaRepository.buscar_boletos(
            numero_boleto=numero_boleto,
            datas_pagamento=datas_pagamento
        )