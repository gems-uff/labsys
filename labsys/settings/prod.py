import dj_database_url

from .base import *


DEBUG=False

#ALLOWED_HOSTS = ['labsys.herokuapp.com']
ALLOWED_HOSTS = ['*']

DATABASES['default']= dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


STATIC_ROOT = 'staticfiles'
