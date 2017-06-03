from django.conf.urls import url

from .import views

app_name = 'patients'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]
