# app/core/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated, Dict, Any
from app.models.schemas.general_schemas import User, UserInDB
from app.core.config import settings
import bcrypt
import json
import os
from app.core.logging import logger

# ============================================
# CARREGAR USUÁRIOS DO JSON
# ============================================

def load_users_from_json() -> Dict[str, Any]:
    """Carrega os usuários do arquivo JSON."""
    json_path = os.path.join(os.path.dirname(__file__), "usuarios_hash.json")

    if not os.path.exists(json_path):
        logger.warning(f"Arquivo de usuários não encontrado: {json_path}")
        return {}

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Converte para dicionário com email como chave
        users_db = {}
        for user in data.get("users", []):
            email = user["email"]
            users_db[email] = {
                "username": email,  # Usamos email como username
                "full_name": user["name"],
                "email": email,
                "hashed_password": user["password_hash"],
                "disabled": user.get("disabled", False),
                "id": user["id"]
            }

        # Adiciona usuário master do .env (se existir)
        if settings.MASTER_USERNAME and settings.MASTER_PASSWORD:
            master_email = settings.MASTER_USERNAME
            if master_email not in users_db:
                salt = bcrypt.gensalt(rounds=12)
                master_hash = bcrypt.hashpw(settings.MASTER_PASSWORD.encode('utf-8'), salt)
                users_db[master_email] = {
                    "username": master_email,
                    "full_name": "Administrador Master",
                    "email": master_email,
                    "hashed_password": master_hash.decode('utf-8'),
                    "disabled": False,
                    "id": 0,
                    "is_master": True
                }

        logger.info(f" Carregados {len(users_db)} usuários do arquivo")
        return users_db

    except Exception as e:
        logger.error(f"❌ Erro ao carregar usuários: {e}")
        return {}

# ============================================
# BANCO DE DADOS DE USUÁRIOS
# ============================================

fake_users_db = load_users_from_json()



# ============================================
# FUNÇÕES DE AUTENTICAÇÃO (COM BCRYPT REAL)
# ============================================

def get_user(db, username: str):
    """Busca usuário pelo email/username."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica a senha usando bcrypt."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        logger.error(f"Erro ao verificar senha: {e}")
        return False

def authenticate_user(db, email: str, password: str):
    """Autentica o usuário pelo email e senha."""
    user = get_user(db, email)
    if not user:
        logger.warning(f"Tentativa de login com email inexistente: {email}")
        return False
    if not verify_password(password, user.hashed_password):
        logger.warning(f"Senha incorreta para: {email}")
        return False
    if user.disabled:
        logger.warning(f"Tentativa de login de usuário desativado: {email}")
        return False

    logger.info(f"✅ Usuário autenticado: {email}")
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

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """Garante que o usuário está ativo."""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo. Contate o administrador."
        )
    return current_user

def reload_users():
    """Recarrega a lista de usuários (útil para testes)."""
    global fake_users_db
    fake_users_db = load_users_from_json()
    logger.info("Lista de usuários recarregada")
