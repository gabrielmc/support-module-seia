from pydantic import BaseModel
from typing import List, Optional


class BoletoProcessadoSchema(BaseModel):
    numero_boleto: str
    codigo_status: str
    status: str
    valor_pago: float
    data_pagamento: Optional[str]
    origem: str


class RetornoArquivoSchema(BaseModel):
    arquivo: str
    total_processados: int
    boletos: List[BoletoProcessadoSchema]
