from .base import *


DEBUG=False

ALLOWED_HOSTS = ['labsys.herokuapp.com']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgresql-closed-68220'
    }
}

STATIC_ROOT = 'staticfiles'
