
import os
from django.core.asgi import get_asgi_application

# Defaults to dev; set DJANGO_SETTINGS_MODULE=settings.prod in production .env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')

application = get_asgi_application()
