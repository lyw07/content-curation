import os
from .settings import *

STORAGE_ROOT = "/contentworkshop_content/storage/"
DB_ROOT = "/contentworkshop_content/databases/"
STATIC_ROOT = "/contentworkshop_static/"

MEDIA_ROOT = STORAGE_ROOT

SITE_ID = int(os.getenv("SITE_ID"))

SESSION_ENGINE = "django.contrib.sessions.backends.db"

DATABASES = {
    'default': {
        'ENGINE':
        'django.db.backends.postgresql_psycopg2',
        'NAME': 'gonano',
        'USER': os.environ.get('DATA_DB_USER'),
        'PASSWORD': os.environ.get('DATA_DB_PASS'),
        'HOST': os.environ.get('DATA_DB_HOST'),
        'PORT': '',
        'CONN_MAX_AGE': 600,
    },
    'export_staging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'export_staging.sqlite3')
    }
}

# celery settings
BROKER_URL = os.getenv("CELERY_BROKER_URL") or BROKER_URL
CELERY_RESULT_BACKEND = (os.getenv("CELERY_RESULT_BACKEND_URL")
                         or CELERY_RESULT_BACKEND)
CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE") or CELERY_TIMEZONE

# email settings
EMAIL_BACKEND = "postmark.backends.PostmarkBackend"
POSTMARK_API_KEY = os.getenv("EMAIL_CREDENTIALS_POSTMARK_API_KEY")

LANGUAGE_CODE = os.getenv("LANGUAGE_CODE") or "en"
