# Django + Node Drizzle Schema Sync Guide

## Problem
Your Node.js app uses Drizzle ORM to manage the PostgreSQL database schema and migrations. Django needs to **read** from the same database but should **NOT** create or modify tables.

## Solution: SQLAlchemy Core (NOT Django ORM)

**We use SQLAlchemy Core instead of Django ORM for Node-owned tables.**

### Why SQLAlchemy Core?
- ✅ No model duplication - tables are reflected from database
- ✅ No Django migrations for Node tables
- ✅ Memory-efficient streaming for large datasets  
- ✅ No ORM overhead

### Architecture

```
Node.js (Drizzle)           Python (Django + SQLAlchemy)
─────────────────           ────────────────────────────
Schema Owner                Read-Only Access
├── migrations/             ├── core/db/engine.py (Connection pool)
├── models/                 ├── core/db/tables.py (Reflection)
└── drizzle.config.ts       └── services/ (Business logic)

        Both use same DATABASE_URL
                    ↓
            PostgreSQL Database
```

### Implementation

**All code is already set up in `core/db/`**

1. **Connection Pool**: `core/db/engine.py`
2. **Table Reflection**: `core/db/tables.py`
3. **Query Helpers**: `core/db/utils.py`

### Usage Example

```python
from core.db import get_connection, get_table
from sqlalchemy import select

# Get Node-owned table
users_table = get_table('users')

# Query it
with get_connection() as conn:
    stmt = select(users_table).where(users_table.c.active == True)
    result = conn.execute(stmt)
    
    for row in result:
        print(row.email)
```

### When Node Updates Schema

**You don't need to do anything!**

- Tables are reflected at runtime
- New columns appear automatically
- No migrations to run in Python
- Just restart the Python service

### Django ORM vs SQLAlchemy Core

| Use Case | Tool |
|----------|------|
| Node-owned tables (users, transactions) | **SQLAlchemy Core** |
| Python-owned tables (ExportJob, RiskScore) | **Django ORM** |

### Complete Guide

See `SQLALCHEMY_GUIDE.md` for:
- Query examples
- Streaming large datasets
- JOINs and aggregations
- Transaction handling

## Summary

1. ✅ Node/Drizzle manages schema and migrations
2. ✅ Python uses SQLAlchemy Core to query Node tables (reflection-based)
3. ✅ Django ORM only for Python-specific tables
4. ✅ Both services share the same `DATABASE_URL`
5. ✅ Zero schema duplication
