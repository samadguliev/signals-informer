from dotenv import load_dotenv
import os
from playhouse.pool import PooledPostgresqlExtDatabase

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