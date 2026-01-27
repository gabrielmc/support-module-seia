import psycopg2
from contextlib import contextmanager
from app.core.config import settings

@contextmanager
def get_db_connection(ambiente: str):
    if ambiente == "DSV":
        conn = psycopg2.connect(
            host=settings.DATABASE_DSV_HOST,
            port=settings.DATABASE_DSV_PORT,
            dbname=settings.DATABASE_DSV_NAME,
            user=settings.DATABASE_DSV_USER,
            password=settings.DATABASE_DSV_PASSWORD,
        )

    elif ambiente == "HML":
        conn = psycopg2.connect(
            host=settings.DATABASE_HML_HOST,
            port=settings.DATABASE_HML_PORT,
            dbname=settings.DATABASE_HML_NAME,
            user=settings.DATABASE_HML_USER,
            password=settings.DATABASE_HML_PASSWORD,
        )
    else:
        raise ValueError("Ambiente inválido. Use: DSV ou HML")

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
