from .base import *


DEBUG=False

ALLOWED_HOSTS = ['labsys.herokuapp.com']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_ROOT = 'staticfiles'
