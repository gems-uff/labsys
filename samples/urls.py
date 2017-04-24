from django.conf.urls import url

from .import views

app_name = 'samples'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
]
