# Server Deployment Manual (PM2 + Gunicorn)

Deploy the Django backend using **Gunicorn** as the WSGI server, managed by **PM2** — matching the Node.js service deployment style.

---

## 1. Prerequisites — Virtual Environment

```bash
# Install Python venv support if missing (Ubuntu/Debian)
sudo apt update
sudo apt install python3-venv python3-full -y


# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies (gunicorn is included in requirements.txt)
pip install -r requirements.txt
```

---

## 2. Environment Variables

```bash
cp .env.example .env
# Fill in production values: SECRET_KEY, DB_*, REDIS_URL, etc.
```

> **Never** commit `.env` to git. Set `DEBUG=False` and a strong `SECRET_KEY` in production.

---

## 3. Database Migrations

```bash
DJANGO_SETTINGS_MODULE=settings.prod python manage.py migrate
DJANGO_SETTINGS_MODULE=settings.prod python manage.py collectstatic --noinput
```

---

## 4. Install PM2 (if not already installed)

```bash
npm install -g pm2
```

---

## 5. Start Django Web Server

```bash

pm2 start ./venv/bin/gunicorn --name "django-backend" -- \
  --workers 3 \
  --bind 0.0.0.0:8000 \
  config.wsgi:application
```

---

## 6. Start Celery Worker

```bash
pm2 start ./venv/bin/celery --name "django-celery" -- \
  -A config worker -l INFO
```

---

## 7. Persist on Reboot

```bash
pm2 save
pm2 startup
# Run the command that pm2 startup prints
```

---

## Useful PM2 Commands

| Action | Command |
|--------|---------|
| View logs (web) | `pm2 logs django-backend` |
| View logs (celery) | `pm2 logs django-celery` |
| Restart web | `pm2 restart django-backend` |
| Restart celery | `pm2 restart django-celery` |
| Status of all | `pm2 status` |
| Stop all | `pm2 stop all` |

---

## Health Check

After starting, verify the server is up:

```bash
curl http://localhost:8000/api/ping/
# Expected: {"status": "ok", "environment": "production"}
```
