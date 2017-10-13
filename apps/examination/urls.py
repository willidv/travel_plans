from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index),
     url(r'^examination/register$', views.register),
    url(r'^examination/login$', views.login),
    url(r'^home$', views.home),
    url(r'^examination/logout$', views.logout),
    url(r'^examination/new$', views.new),
    url(r'^examination/add$', views.add),
    url(r'^plan/(?P<id>\w+)$', views.plan),
    url(r'^join/(?P<id>\w+)$', views.join),
]