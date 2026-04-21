"""
SQLAlchemy engine configuration for accessing Node/Drizzle-owned PostgreSQL tables.

This module provides a centralized database connection pool that bypasses Django ORM
for Node-managed schema. Use this for:
- Reading Node tables (users, transactions, etc.)
- Bulk data exports
- Analytics queries

DO NOT use this for Python-owned tables - use Django ORM instead.
"""

import os
from sqlalchemy import create_engine, event
from sqlalchemy.pool import QueuePool

# Database URL from environment (same as Django uses)
# In settings/base.py, we construct this from individual vars if needed
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    # Fallback construction similar to settings
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'testdb')
    DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,              # Number of connections to keep open
    max_overflow=20,           # Additional connections when pool is exhausted
    pool_timeout=30,           # Seconds to wait for connection
    pool_pre_ping=True,        # Verify connections before using
    pool_recycle=3600,         # Recycle connections after 1 hour
    echo=False,                # Set to True for SQL query logging (dev only)
    future=True                # Use SQLAlchemy 2.0 style
)


@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Set connection parameters on new connections."""
    pass  # Add any connection-level config here if needed


def get_connection():
    """
    Get a database connection from the pool.
    
    Usage:
        with get_connection() as conn:
            result = conn.execute(select(users_table))
    """
    return engine.connect()


def dispose_engine():
    """
    Dispose of the connection pool.
    Call this during application shutdown.
    """
    engine.dispose()
