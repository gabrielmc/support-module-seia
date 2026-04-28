# app/core/db_pool.py
from psycopg2 import pool
from contextlib import contextmanager
from app.core.config import settings
from app.core.logging import logger

# ============================================
# POOLS DE CONEXÃO POR AMBIENTE
# ============================================

class DatabasePools:
    """Gerencia pools de conexão por ambiente."""

    def __init__(self):
        self.pools = {}
        self.min_connections = 5   # Mínimo de conexões por pool
        self.max_connections = 20  # Máximo de conexões por pool

    def _get_pool(self, ambiente: str):
        """Retorna o pool do ambiente (cria se não existir)."""
        if ambiente not in self.pools:
            self.pools[ambiente] = self._create_pool(ambiente)
        return self.pools[ambiente]

    def _create_pool(self, ambiente: str):
        """Cria um novo pool de conexões."""
        if ambiente == "DSV":
            config = {
                "host": settings.DATABASE_DSV_HOST,
                "port": settings.DATABASE_DSV_PORT,
                "dbname": settings.DATABASE_DSV_NAME,
                "user": settings.DATABASE_DSV_USER,
                "password": settings.DATABASE_DSV_PASSWORD,
            }
        elif ambiente == "HML":
            config = {
                "host": settings.DATABASE_HML_HOST,
                "port": settings.DATABASE_HML_PORT,
                "dbname": settings.DATABASE_HML_NAME,
                "user": settings.DATABASE_HML_USER,
                "password": settings.DATABASE_HML_PASSWORD,
            }
        elif ambiente == "TRT":
            config = {
                "host": settings.DATABASE_TREINAMENTO_HOST,
                "port": settings.DATABASE_TREINAMENTO_PORT,
                "dbname": settings.DATABASE_TREINAMENTO_NAME,
                "user": settings.DATABASE_TREINAMENTO_USER,
                "password": settings.DATABASE_TREINAMENTO_PASSWORD,
            }
        else:
            raise ValueError("Ambiente inválido. Use: DSV, HML ou TRT")

        logger.info(f"🚀 Criando pool para ambiente {ambiente} (min={self.min_connections}, max={self.max_connections})")
        return pool.SimpleConnectionPool(
            self.min_connections,
            self.max_connections,
            **config
        )

    @contextmanager
    def get_connection(self, ambiente: str):
        """Obtém uma conexão do pool."""
        pool = self._get_pool(ambiente)
        conn = pool.getconn()
        conn.autocommit = True # Otimização: auto-commit para operações de leitura
        try:
            yield conn
        finally:
            pool.putconn(conn) # Devolve a conexão ao pool (não fecha!)

    def close_all_pools(self):
        """Fecha todos os pools (chamar no shutdown da aplicação)."""
        for ambiente, pool in self.pools.items():
            logger.info(f" Fechando pool do ambiente {ambiente}")
            pool.closeall()

# Instância global
db_pools = DatabasePools()