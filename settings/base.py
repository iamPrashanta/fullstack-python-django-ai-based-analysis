
from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add apps to sys.path - Removed to avoid conflicts
# sys.path.append(str(BASE_DIR / 'apps'))

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-change-in-prod')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
# Pure API Configuration - No Admin, No UI
INSTALLED_APPS = [
    # Minimal Django Apps
    'django.contrib.auth',          # Required for DRF Token/User
    'django.contrib.contenttypes',  # Required for Auth/Permissions
    'django.contrib.sessions',      # Required for UI
    'django.contrib.messages',      # Required for UI
    'django.contrib.staticfiles',   # Required for UI
    'django.contrib.admin',         # Required for UI

    # Third Party
    'rest_framework',
    'corsheaders',
    'django_celery_results',

    # Domain Apps
    'core',
    'apps.analytics',
    'apps.ml_models',
    'apps.exhibitors',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    
    # Security Setup
    'django.middleware.security.SecurityMiddleware',
    
    # Core Request Handling
    'django.middleware.common.CommonMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# TEMPLATES configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'config.wsgi.application'

# ── Primary Database (Main PostgreSQL — shared with Node/Drizzle) ────────────
DB_USER     = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST     = os.getenv('DB_HOST', 'localhost')
DB_PORT     = os.getenv('DB_PORT', '5432')
DB_NAME     = os.getenv('DB_NAME', 'testdb')

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    DATABASE_URL = f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    os.environ['DATABASE_URL'] = DATABASE_URL  # Picked up by SQLAlchemy engine too

# ── Vector Database (pgvector — AI embeddings & ML results) ─────────────────
VECTOR_DB_USER     = os.getenv('VECTOR_DB_USER', DB_USER)
VECTOR_DB_PASSWORD = os.getenv('VECTOR_DB_PASSWORD', 'SecurePass1234')
VECTOR_DB_HOST     = os.getenv('VECTOR_DB_HOST', DB_HOST)
VECTOR_DB_PORT     = os.getenv('VECTOR_DB_PORT', '5433')
VECTOR_DB_NAME     = os.getenv('VECTOR_DB_NAME', 'vector_db')

VECTOR_DATABASE_URL = os.getenv('VECTOR_DATABASE_URL')
if not VECTOR_DATABASE_URL:
    VECTOR_DATABASE_URL = (
        f"postgres://{VECTOR_DB_USER}:{VECTOR_DB_PASSWORD}"
        f"@{VECTOR_DB_HOST}:{VECTOR_DB_PORT}/{VECTOR_DB_NAME}"
    )
    os.environ['VECTOR_DATABASE_URL'] = VECTOR_DATABASE_URL

DATABASES = {
    # Main DB — Django ORM for Python-owned tables + SQLAlchemy for Node tables
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    ),
    # Vector DB — pgvector, used exclusively by apps.ml_models
    'vector_db': dj_database_url.parse(
        VECTOR_DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    ),
}

# Database Routers
# Order matters: VectorDbRouter checked first, then ReadReplicaRouter
DATABASE_ROUTERS = [
    'core.db_routers.VectorDbRouter',    # Routes ml_models app → vector_db
    'core.db_routers.ReadReplicaRouter', # Everything else → default
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DRF Configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# Celery Configuration
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TRACK_STARTED = True
