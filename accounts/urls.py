from django.conf.urls import url
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView


from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^logout_lander/', views.logoutLander, name='logout_lander'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<user_id>[0-9]+)', views.other_profile, name="other_profile"),
]
