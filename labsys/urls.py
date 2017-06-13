import os

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


core_urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

my_urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^samples/', include('samples.urls')),
    url(r'^admission_notes/', include('admission_notes.urls')),
]


urlpatterns = core_urlpatterns + my_urlpatterns

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


if 'nested_admin' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^_nested_admin/', include('nested_admin.urls')),
    ]
