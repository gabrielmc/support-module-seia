from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

# IMPORTANTE: Ajuste este import para o local correto do seu arquivo security.py
from app.core.security import fake_users_db, authenticate_user

router = APIRouter(tags=["AUTENTICAÇÃO"])

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Endpoint público para o usuário (ex: 'admin_master') obter um token Bearer.
    - **username**: Nome do usuário
    - **password**: Senha do usuário

    Retorna um token simples (o próprio nome do usuário) para ser usado no header:
    `Authorization: Bearer admin_master`
    """
    # 1. Autentica o usuário usando username e password (form data)
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Em uma implementação REAL, você geraria um JWT token aqui.
    # Nesta versão SIMPLES, o token é o próprio 'username'.
    return {"access_token": user.username, "token_type": "bearer"}