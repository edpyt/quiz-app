from .settings import *


DEBUG = False

SECRET_KEY = ')quu=de+1fze++3&_^&mtg)xckmht79d1mm8b)20v14_^1=3xd'

ALLOWED_HOSTS = ['*']

# Change to Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}