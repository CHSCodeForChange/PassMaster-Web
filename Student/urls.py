from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^request/', views.requestPass),
    url(r'^viewPass', views.viewPass),
]