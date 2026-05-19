# app/routes/autenticacao_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.core.security import fake_users_db, authenticate_user
from app.core.logging import logger

router = APIRouter(tags=["Autenticação"])

@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Endpoint para autenticação de usuários.
    - **username**: Email do usuário (ex: gabriel.cerqueira@prodeb)
    - **password**: Senha do usuário (ex: seia@123)
    Retorna um token Bearer para ser usado no header:
    `Authorization: Bearer <email_do_usuario>`
    """
    # Autentica usando email (username) e senha
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info(f"🔐 Login realizado: {user.username}")
    # Retorna o email como token (versão simples)
    # Em produção, use JWT!
    return {
        "access_token": user.username,
        "token_type": "bearer",
        "user": {
            "id": getattr(user, 'id', None),
            "name": user.full_name,
            "email": user.username
        }
    }
