from .settings import *


DEBUG = False

SECRET_KEY = ''

ALLOWED_HOSTS = ['*']

# Change to Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}