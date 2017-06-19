import os

from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from rest_framework import routers

from collected_sample import views


router = routers.DefaultRouter()
router.register(r'collection_methods', views.CollectionMethodViewSet)

core_urlpatterns = [
    url(r'^admin/', admin.site.urls),
]

my_urlpatterns = [
    url(r'^', include(router.urls)),
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
