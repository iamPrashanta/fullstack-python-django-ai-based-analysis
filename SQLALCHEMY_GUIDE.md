# SQLAlchemy Core Usage Guide

This guide shows how to use SQLAlchemy Core (not ORM) to query Node/Drizzle-owned PostgreSQL tables.

## Why SQLAlchemy Core?

- **Node owns schema**: Drizzle manages migrations, Python only reads/processes data
- **No model duplication**: Tables are reflected from database at runtime
- **Memory efficient**: Stream large datasets without loading all rows
- **No ORM overhead**: Direct SQL queries with Python API

## Basic Usage

### 1. Get a Table

```python
from core.db import get_table

# Reflect a Node-owned table
users_table = get_table('users')
transactions_table = get_table('transactions')
```

### 2. Simple SELECT

```python
from sqlalchemy import select
from core.db import get_connection, get_table

users_table = get_table('users')

with get_connection() as conn:
    # Select all users
    stmt = select(users_table)
    result = conn.execute(stmt)
    
    for row in result:
        print(row.email, row.name)
```

### 3. WHERE Clause

```python
from sqlalchemy import select

users_table = get_table('users')

with get_connection() as conn:
    # Filter users
    stmt = select(users_table).where(
        users_table.c.active == True,
        users_table.c.email.like('%@gmail.com')
    )
    result = conn.execute(stmt)
```

### 4. Streaming Large Datasets

```python
from core.db import get_connection, get_table, stream_query

transactions_table = get_table('transactions')
stmt = select(transactions_table)

with get_connection() as conn:
    # Process in batches of 5000
    for batch in stream_query(conn, stmt, batch_size=5000):
        process_batch(batch)  # batch is a list of dicts
```

### 5. Aggregations

```python
from sqlalchemy import select, func

users_table = get_table('users')

with get_connection() as conn:
    # Count users
    stmt = select(func.count()).select_from(users_table)
    count = conn.execute(stmt).scalar()
    
    # Group by status
    stmt = select(
        users_table.c.status,
        func.count(users_table.c.id).label('count')
    ).group_by(users_table.c.status)
    
    result = conn.execute(stmt)
    for row in result:
        print(f"{row.status}: {row.count}")
```

### 6. JOINs

```python
from sqlalchemy import select

users_table = get_table('users')
transactions_table = get_table('transactions')

with get_connection() as conn:
    stmt = select(
        users_table.c.email,
        transactions_table.c.amount,
        transactions_table.c.status
    ).select_from(
        users_table.join(
            transactions_table,
            users_table.c.id == transactions_table.c.user_id
        )
    ).where(
        transactions_table.c.amount > 100
    )
    
    result = conn.execute(stmt)
```

### 7. UPDATE (Use Sparingly)

```python
from sqlalchemy import update

export_jobs_table = get_table('export_jobs')

with get_connection() as conn:
    stmt = update(export_jobs_table).where(
        export_jobs_table.c.id == job_id
    ).values(
        status='completed',
        file_url=s3_url
    )
    
    conn.execute(stmt)
    conn.commit()
```

### 8. Transactions

```python
from core.db import get_connection, execute_in_transaction

def operation1(conn):
    stmt = update(table1).where(...).values(...)
    conn.execute(stmt)

def operation2(conn):
    stmt = insert(table2).values(...)
    conn.execute(stmt)

with get_connection() as conn:
    execute_in_transaction(conn, [operation1, operation2])
```

## Converting Django ORM to SQLAlchemy Core

### Django ORM
```python
# Django
users = User.objects.filter(active=True, email__contains='gmail')
for user in users:
    print(user.email)
```

### SQLAlchemy Core
```python
# SQLAlchemy Core
users_table = get_table('users')

with get_connection() as conn:
    stmt = select(users_table).where(
        users_table.c.active == True,
        users_table.c.email.like('%gmail%')
    )
    result = conn.execute(stmt)
    for row in result:
        print(row.email)
```

## Best Practices

1. **Use `get_connection()` context manager** - ensures connections are returned to pool
2. **Stream large results** - use `stream_query()` for exports
3. **Reflection is cached** - first call reflects, subsequent calls use cache
4. **Commit explicitly** - connections don't auto-commit
5. **Keep Django ORM for Python tables** - only use SQLAlchemy for Node tables

## Examples

See `services/export_service.py` for a complete example of:
- Streaming large datasets
- Building dynamic filters
- Generating CSV exports
- Uploading to S3
