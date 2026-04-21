
import os
from django.core.wsgi import get_wsgi_application

# Defaults to dev; set DJANGO_SETTINGS_MODULE=settings.prod in production .env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')

application = get_wsgi_application()
