from dotenv import load_dotenv
from contextlib import contextmanager
from playhouse.pool import PooledPostgresqlExtDatabase
import os

load_dotenv()

# Database configuration
DATABASE = {
    'name': os.getenv("POSTGRES_DB"),
    'user': os.getenv("POSTGRES_USER"),
    'password': os.getenv("POSTGRES_PASSWORD"),
    'host': 'pg_db',
    'port': 5432,
}

# Configure connection pool
db = PooledPostgresqlExtDatabase(
    DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port'],
    max_connections=20,
    stale_timeout=300,  # 5 minutes
)


@contextmanager
def get_db_connection():
    db.connect(reuse_if_open=True)
    try:
        yield db
    finally:
        if not db.is_closed():
            db.close()
