from pydantic import BaseModel, Field

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
