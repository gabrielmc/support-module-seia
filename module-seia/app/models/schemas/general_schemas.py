from pydantic import BaseModel, Field
from typing import List

class RepflorRequest(BaseModel):
    identificador: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="String identificadora para consulta no REPLFOR"
    )

class RepflorResponse(BaseModel):
    encontrado: bool
    status: int | None = None
    update_script: str | None = None

class ExcluirRequerimentoLogico(BaseModel):
    requerente: str = Field(..., example="JOÃO DA SILVA")
    cpf_cnpj: str = Field(..., example="12345678901")
    imovel: str = Field(..., example="FAZENDA BOA VISTA")

class UsuarioEmail(BaseModel):
    cpf: str = Field(..., example="08512197560")
    email: str = Field(..., example="usuario@email.com")

class ListaUsuariosEmail(BaseModel):
    usuarios: List[UsuarioEmail]

class UsuarioScriptCPF(BaseModel):
    ticket : str
    cpf: str
    email: str

class ListaUsuariosCPF(BaseModel):
    usuarios: List[UsuarioScriptCPF]

class UsuarioPerfil(BaseModel):
    usuario: str = Field(..., example="JOÃO DA SILVA")
    perfil: int = Field(..., example=9)
