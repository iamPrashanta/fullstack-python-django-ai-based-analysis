"""
Core database module for SQLAlchemy Core integration.

This module provides direct SQL access to PostgreSQL tables managed by Node/Drizzle.
Use this instead of Django ORM for Node-owned tables.
"""

from .engine import engine, get_connection, dispose_engine
from .tables import metadata, reflect_table, get_table
from .utils import stream_query, execute_in_transaction, row_to_dict, execute_scalar

__all__ = [
    'engine',
    'get_connection',
    'dispose_engine',
    'metadata',
    'reflect_table',
    'get_table',
    'stream_query',
    'execute_in_transaction',
    'row_to_dict',
    'execute_scalar',
]
