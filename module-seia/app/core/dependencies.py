from fastapi import Depends
from app.core.security import get_current_active_user

# Cria uma dependência reutilizável
CommonAuth = Depends(get_current_active_user)