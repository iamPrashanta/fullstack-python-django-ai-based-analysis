# Project Structure & API Guide

Architecture of the Django backend — folder responsibilities and available API routes.

## Actual Folder Structure

```
python-django/
├── manage.py                    # Django CLI entry point
├── requirements.txt             # Python dependencies
├── .env                         # Local env vars (never commit)
├── .env.example                 # Template for env vars
├── Dockerfile
├── docker-compose.yml
│
├── config/                      # Django config root (wsgi, urls, celery)
│   ├── urls.py                  # Root URL routing
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py                # Celery app definition
│
├── settings/                    # Split settings
│   ├── base.py                  # Common settings (DB, Celery, DRF)
│   ├── dev.py                   # DEBUG=True, relaxed CORS
│   └── prod.py                  # DEBUG=False, JSON logging, security headers
│
├── core/                        # Shared utilities and base models
│   ├── models.py                # TimestampedModel (abstract base)
│   ├── views.py                 # /api/health/, /api/test-db/
│   ├── utils.py                 # Shared helpers
│   ├── db_routers.py            # Read-replica routing
│   └── db/                      # SQLAlchemy Core (Node table access)
│       ├── engine.py            # Connection pool
│       ├── tables.py            # Table reflection
│       └── utils.py             # stream_query, execute_in_transaction
│
├── apps/                        # Domain modules (Django apps)
│   ├── analytics/               # Dashboard aggregations
│   ├── ml_models/               # ML registry + inference
│   └── exhibitors/              # Exhibitor-specific logic
│
├── services/                    # External service wrappers
│   ├── s3.py                    # AWS S3 upload / presigned URLs
│   ├── ses.py                   # AWS SES email
│   └── export_service.py        # SQLAlchemy-based CSV export to S3
│
└── api/                         # Legacy/simple API app (ping, health)
    ├── views.py
    └── urls.py
```

---

## API Endpoints

### System (core/views.py)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/ping/` | Basic liveness check. No auth required. |
| GET | `/api/health/` | DB + cache + celery status. |
| GET | `/api/test-db/` | Explicit DB connectivity test (admin only). |

### Analytics (apps/analytics)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/analytics/dashboard/` | High-level dashboard stats. |
| GET | `/api/analytics/volume/` | Transaction volume time-series. |

### ML Models (apps/ml_models)
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/ml/train/` | Trigger model training (internal/admin). |
| POST | `/api/ml/predict/` | Run inference on input data. |

### Exhibitors (apps/exhibitors)
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/exhibitors/` | List exhibitors. |

---

## Infrastructure Connections

### PostgreSQL
- Config: `settings/base.py` — builds `DATABASE_URL` from individual `DB_*` env vars.
- Node (Drizzle) **owns** the schema and migrations.
- Django reads Node-owned tables via **SQLAlchemy Core** (`core/db/`) — no migrations needed.
- Django ORM manages only Python-owned tables (`ExportJob`, `RiskScore`, etc.).

### Redis
- Celery broker: `CELERY_BROKER_URL` (default `redis://127.0.0.1:6379/1`)
- Celery results: `CELERY_RESULT_BACKEND`
- Cache: configured in `settings/base.py`

### Celery Workers
- App name: `config` (defined in `config/celery.py`)
- Start: `celery -A config worker -l INFO`
- Tasks auto-discovered from all `INSTALLED_APPS`

---

## Reference Docs
- `SCHEMA_SYNC_GUIDE.md` — Why SQLAlchemy Core is used for Node tables
- `SQLALCHEMY_GUIDE.md` — Query patterns, streaming, JOINs, transactions
- `START_MANUAL.md` — Production deployment with Gunicorn + PM2
