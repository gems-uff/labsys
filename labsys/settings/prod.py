import dj_database_url

from .base import *


# TODO: Serve files via a dedicated static server then change this value
DEBUG=False

ALLOWED_HOSTS = ['labsys.herokuapp.com']

DATABASES['default'] = dj_database_url.config()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATIC_ROOT = 'staticfiles'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static')
)