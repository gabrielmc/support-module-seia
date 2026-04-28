from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from app.models.schemas.general_schemas import User, UserInDB
from app.core.config import settings


# Dicionário do usuário master
fake_users_db = {
    settings.MASTER_USERNAME: {
        "username": settings.MASTER_USERNAME,
        "full_name": "Administrador Master",
        "email": "gabriel.cerqueira@prodeb.ba.gov.br",
        "hashed_password": f"fakehashed{settings.MASTER_PASSWORD}",
        "disabled": False,
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# --- Funções de Autenticação Fake (sem JWT por enquanto) ---
def fake_hash_password(password: str):
    """Simula o hashing de senha."""
    return "fakehashed" + password

def verify_password(plain_password: str, hashed_password: str):
    """Verifica a senha (fake)."""
    return fake_hash_password(plain_password) == hashed_password

def authenticate_user(db, username: str, password: str):
    """Autentica o usuário pelo username e senha."""
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# ============================================
# CONFIGURAÇÃO OATH2
# ============================================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Valida o token e retorna o usuário."""
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = get_user(fake_users_db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    """Garante que o usuário está ativo."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user