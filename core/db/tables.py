"""
Reflected table definitions for Node/Drizzle-owned PostgreSQL tables.

These tables are auto-discovered from the database schema at runtime.
DO NOT define columns manually - they are reflected from the actual schema.

Add new tables here as needed for your queries.
"""

from sqlalchemy import MetaData, Table
from .engine import engine

# Metadata container for all reflected tables
metadata = MetaData()

# Reflect Node-owned tables
# Add more tables as needed by your application

# Example: users table (uncomment and modify based on your schema)
# users_table = Table('users', metadata, autoload_with=engine)

# Example: transactions table
# transactions_table = Table('transactions', metadata, autoload_with=engine)

# Example: accounts table
# accounts_table = Table('accounts', metadata, autoload_with=engine)


def reflect_table(table_name: str) -> Table:
    """
    Dynamically reflect a table from the database.
    
    Args:
        table_name: Name of the table in PostgreSQL
        
    Returns:
        SQLAlchemy Table object
        
    Usage:
        users = reflect_table('users')
        stmt = select(users).where(users.c.id == '123')
    """
    return Table(table_name, metadata, autoload_with=engine)


def get_table(table_name: str) -> Table:
    """
    Get a table from metadata or reflect it if not already loaded.
    
    Args:
        table_name: Name of the table in PostgreSQL
        
    Returns:
        SQLAlchemy Table object
    """
    if table_name in metadata.tables:
        return metadata.tables[table_name]
    return reflect_table(table_name)
