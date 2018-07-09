from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^(?P<pass_id>[0-9]+)/$', views.approve, name='approve'), 
]
