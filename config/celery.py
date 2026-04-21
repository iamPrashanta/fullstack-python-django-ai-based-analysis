
import os
from celery import Celery

# Use DJANGO_SETTINGS_MODULE from environment.
# Defaults to 'settings.dev' locally — set to 'settings.prod' on the server
# via the .env file or PM2 env config.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')

app = Celery('config')

# Pull all CELERY_* keys from Django settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py in every INSTALLED_APP.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
