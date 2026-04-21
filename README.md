# Django Data Analysis Backend

Python/Django backend for data analysis, ML inference, and analytics. Sits alongside the Node.js backend, sharing the same PostgreSQL database. Node (Drizzle) owns the schema; Django reads Node tables via SQLAlchemy Core and manages its own tables via Django ORM.

## Project Structure

```
python-django/
├── config/                 # Django config root
│   ├── urls.py             # Root URL routing
│   ├── wsgi.py             # WSGI entry point
│   ├── asgi.py             # ASGI entry point
│   └── celery.py           # Celery app definition
├── settings/               # Split settings
│   ├── base.py             # Common (DB, Celery, DRF, CORS)
│   ├── dev.py              # DEBUG=True, relaxed security
│   └── prod.py             # DEBUG=False, JSON logging, security headers
├── core/                   # Shared utilities & base models
│   ├── models.py           # TimestampedModel (abstract base)
│   ├── views.py            # /api/health/, /api/test-db/
│   ├── db_routers.py       # Read-replica routing
│   └── db/                 # SQLAlchemy Core for Node-owned tables
│       ├── engine.py       # Connection pool
│       ├── tables.py       # Table reflection
│       └── utils.py        # stream_query, execute_in_transaction
├── apps/                   # Domain modules
│   ├── analytics/          # Aggregation services, dashboard APIs
│   ├── ml_models/          # Model registry + inference service
│   └── exhibitors/         # Exhibitor-specific logic
├── services/               # External service wrappers
│   ├── s3.py               # AWS S3 upload / presigned URLs
│   ├── ses.py              # AWS SES email
│   └── export_service.py   # SQLAlchemy streaming CSV → S3
├── manage.py
└── requirements.txt
```

## Prerequisites

- Python 3.11+
- PostgreSQL (shared with Node backend)
- Redis (Celery broker + cache)

## Local Development Setup

### 1. Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
.\venv\Scripts\activate         # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

```bash
cp .env.example .env
# Edit .env with your local DB credentials and Redis URL
```

Required variables:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local, `False` for production |
| `ALLOWED_HOSTS` | Comma-separated hosts |
| `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` / `DB_NAME` | PostgreSQL credentials |
| `REDIS_URL` | Redis connection string |
| `CELERY_BROKER_URL` | Celery broker (usually same as REDIS_URL) |
| `CELERY_RESULT_BACKEND` | Celery result store |

### 4. Run Migrations

```bash
# Django ORM manages only Python-owned tables
DJANGO_SETTINGS_MODULE=settings.dev python manage.py migrate
```

### 5. Start Services

```bash
# Web server
DJANGO_SETTINGS_MODULE=settings.dev python manage.py runserver

# Celery worker (separate terminal)
celery -A config worker -l INFO
```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/ping/` | Liveness check |
| GET | `/api/health/` | DB + cache + celery status |
| GET | `/api/analytics/dashboard/` | Dashboard stats |
| GET | `/api/analytics/volume/` | Volume time-series |
| POST | `/api/ml/predict/` | Run ML inference |

See `API_STRUCTURE.md` for the full endpoint reference.

## Database Strategy

| Table ownership | Tool |
|-----------------|------|
| Node/Drizzle tables (users, transactions, …) | **SQLAlchemy Core** — reflected at runtime, zero migrations |
| Python-owned tables (ExportJob, RiskScore, …) | **Django ORM** |

See `SCHEMA_SYNC_GUIDE.md` and `SQLALCHEMY_GUIDE.md` for patterns.

## Production Deployment

Using **Gunicorn** as WSGI server, managed by **PM2**:

```bash
# Web server
pm2 start ./venv/bin/gunicorn --name "django-backend" -- \
  --workers 3 --bind 0.0.0.0:8000 config.wsgi:application

# Celery worker
pm2 start ./venv/bin/celery --name "django-celery" -- \
  -A config worker -l INFO

pm2 save && pm2 startup
```

See `START_MANUAL.md` for the full step-by-step server setup guide.
