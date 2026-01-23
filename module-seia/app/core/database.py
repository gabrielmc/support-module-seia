import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.core.config import settings

@contextmanager
def get_db_connection():
    connect = psycopg2.connect(
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        dbname=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD
    )
    try:
        yield connect
        connect.commit()
    except Exception:
        connect.rollback()
        raise
    finally:
        connect.close()