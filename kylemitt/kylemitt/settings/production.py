from .base import *

DEBUG = False

ALLOWED_HOSTS = ['165.22.126.182', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kylemitt',
        'USER': 'kylemitt',
        'PASSWORD': 'kylemitt',
        'HOST': 'localhost',
        'PORT': '',
    }
}
