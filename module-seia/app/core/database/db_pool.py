# app/core/database/db_pool.py

from psycopg2 import pool
from contextlib import contextmanager
from app.core.config import settings
from app.core.logging import logger
import time

# ============================================
# POOLS DE CONEXÃO POR AMBIENTE
# ============================================

class DatabasePools:
    """Gerencia pools de conexão por ambiente."""

    def __init__(self):
        self.pools = {}
        self.min_connections = 5
        self.max_connections = 20
        self.max_retries = 3
        self.retry_delay = 1

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

        # Configurações keepalive para evitar timeout
        config["keepalives"] = 1
        config["keepalives_idle"] = 30
        config["keepalives_interval"] = 10
        config["keepalives_count"] = 5
        try:
            # Cria o pool com autocommit já ativado via connection_factory
            return pool.SimpleConnectionPool(
                self.min_connections,
                self.max_connections,
                **config
            )
        except Exception as e:
            logger.error(f"❌ Erro ao criar pool para {ambiente}: {e}")
            raise

    def _is_connection_valid(self, conn):
        """Verifica se a conexão está saudável."""
        if conn is None or conn.closed:
            return False
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return True
        except Exception:
            return False

    def _set_autocommit_cleanly(self, conn):
        """Define autocommit de forma segura, sem transação ativa."""
        try:
            # Verifica se já está em autocommit
            if conn.autocommit:
                return
            # Método correto: usar set_session com autocommit
            conn.set_session(autocommit=True)
            logger.debug("✅ Autocommit ativado com sucesso")
        except Exception as e:
            # Se falhar, tenta fazer rollback primeiro para limpar transação pendente
            try:
                conn.rollback()
                conn.set_session(autocommit=True)
            except Exception as e2:
                logger.error(f"❌ Falha ao ativar autocommit: {e2}")
                raise

    @contextmanager
    def get_connection(self, ambiente: str):
        """Obtém uma conexão válida do pool."""
        pool_obj = self._get_pool(ambiente)
        conn = None

        for attempt in range(self.max_retries):
            try:
                # Obtém a conexão do pool
                conn = pool_obj.getconn()

                # Verifica se a conexão está saudável
                if not self._is_connection_valid(conn):
                    logger.warning(f"⚠️ Conexão inválida para {ambiente}, tentativa {attempt + 1}")
                    pool_obj.putconn(conn)
                    if attempt == self.max_retries - 1:
                        self._recreate_pool(ambiente)
                        pool_obj = self._get_pool(ambiente)
                    continue

                # CORREÇÃO: Define autocommit de forma segura
                self._set_autocommit_cleanly(conn)

                yield conn
                return  # Sai do loop após sucesso

            except Exception as e:
                logger.error(f"❌ Erro na tentativa {attempt + 1} para {ambiente}: {e}")
                # Tenta devolver a conexão ao pool se existir
                if conn:
                    try:
                        pool_obj.putconn(conn)
                    except Exception as put_err:
                        logger.warning(f"Erro ao devolver conexão: {put_err}")

                if attempt == self.max_retries - 1:
                    raise
                time.sleep(self.retry_delay)
            finally:
                # Garante que a conexão seja devolvida ao pool
                if conn and not conn.closed:
                    try:
                        pool_obj.putconn(conn)
                    except Exception as e:
                        logger.warning(f"Erro ao devolver conexão: {e}")

    def _recreate_pool(self, ambiente: str):
        """Recria o pool para um ambiente específico."""
        if ambiente in self.pools:
            try:
                old_pool = self.pools[ambiente]
                old_pool.closeall()
            except Exception as e:
                logger.warning(f"Erro ao fechar pool antigo {ambiente}: {e}")

        self.pools[ambiente] = self._create_pool(ambiente)
        logger.info(f"✅ Pool recriado para ambiente {ambiente}")

    def close_all_pools(self):
        """Fecha todos os pools (chamar no shutdown da aplicação)."""
        for ambiente, pool_obj in self.pools.items():
            try:
                pool_obj.closeall()
            except Exception as e:
                logger.warning(f"Erro ao fechar pool {ambiente}: {e}")

# Instância global
db_pools = DatabasePools()
