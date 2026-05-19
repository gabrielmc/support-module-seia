from contextlib import contextmanager
from app.core.database.db_pool import db_pools
from app.core.logging import logger


@contextmanager
def get_db_connection(ambiente: str):
    """
    Obtém uma conexão do pool (RÁPIDO!).
    Use em TODAS as suas rotas no lugar da conexão direta.
    """
    try:
        with db_pools.get_connection(ambiente) as conn:
            yield conn
    except Exception as e:
        logger.error(f"Erro ao obter conexão do pool ({ambiente}): {e}")
        raise

def close_all_db_pools():
    db_pools.close_all_pools()