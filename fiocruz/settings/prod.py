from .base import *


# TODO: Serve files via a dedicated static server then change this value
DEBUG=True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fiocruz_prod'
    }
}
