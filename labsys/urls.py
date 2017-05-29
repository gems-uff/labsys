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
]

api_urls = [
    url(r'^', include('snippets.urls')),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

urlpatterns = core_urlpatterns + my_urlpatterns + api_urls


if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
