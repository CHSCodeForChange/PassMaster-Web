from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^hello/(?P<stuff>[\w\-]+)/$', views.home),
    url(r'^login_api/(?P<username>[\w\-]+)/(?P<password>[\w\-]+)', views.post),
]