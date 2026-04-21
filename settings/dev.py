
from .base import *

DEBUG = True

# Allow all hosts in dev
ALLOWED_HOSTS = ['*']

# Console logging for dev
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Dev-specific third-party apps
# INSTALLED_APPS += ['debug_toolbar'] # Uncomment if needed
