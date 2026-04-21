"""
Utility functions for working with SQLAlchemy Core queries.

Provides helpers for:
- Streaming large datasets
- Transaction management
- Row processing
"""

from typing import Iterator, Dict, Any, List
from sqlalchemy import select
from sqlalchemy.engine import Connection, Result


def stream_query(conn: Connection, stmt, batch_size: int = 1000) -> Iterator[List[Dict[str, Any]]]:
    """
    Execute a query and yield results in batches for memory-efficient processing.
    
    Args:
        conn: SQLAlchemy connection
        stmt: SQLAlchemy select statement
        batch_size: Number of rows per batch
        
    Yields:
        List of row dictionaries
        
    Usage:
        stmt = select(users_table).where(users_table.c.active == True)
        with get_connection() as conn:
            for batch in stream_query(conn, stmt, batch_size=5000):
                process_batch(batch)
    """
    result = conn.execution_options(stream_results=True, max_row_buffer=batch_size).execute(stmt)
    
    while True:
        batch = result.fetchmany(batch_size)
        if not batch:
            break
        yield [dict(row._mapping) for row in batch]


def execute_in_transaction(conn: Connection, operations: List[callable]) -> None:
    """
    Execute multiple operations within a single transaction.
    
    Args:
        conn: SQLAlchemy connection
        operations: List of callable functions that take connection as argument
        
    Raises:
        Exception: Any exception will rollback the transaction
        
    Usage:
        def insert_records(conn):
            conn.execute(insert(table).values(...))
            
        def update_status(conn):
            conn.execute(update(table).where(...).values(...))
            
        with get_connection() as conn:
            execute_in_transaction(conn, [insert_records, update_status])
    """
    with conn.begin():
        for operation in operations:
            operation(conn)


def row_to_dict(result: Result) -> List[Dict[str, Any]]:
    """
    Convert SQLAlchemy result to list of dictionaries.
    
    Args:
        result: SQLAlchemy result object
        
    Returns:
        List of row dictionaries
    """
    return [dict(row._mapping) for row in result]


def execute_scalar(conn: Connection, stmt) -> Any:
    """
    Execute a statement and return a single scalar value.
    
    Args:
        conn: SQLAlchemy connection
        stmt: SQLAlchemy select statement
        
    Returns:
        Single value or None
        
    Usage:
        stmt = select(func.count()).select_from(users_table)
        count = execute_scalar(conn, stmt)
    """
    return conn.execute(stmt).scalar()
