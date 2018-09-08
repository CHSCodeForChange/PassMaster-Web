from django.conf.urls import url
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView


from . import views

urlpatterns = [
    url(r'^logout_lander/', views.logoutLander, name='logout_lander'),
    url(r'^signup', views.signup, name='signup')
]
