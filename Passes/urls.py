from django.conf.urls import url, include

from . import views
from . import api

from rest_framework import routers

urlpatterns = [
    url(r'^api/passes/$', api.PassList.as_view()),
    url(r'^api/passes/(?P<pk>[0-9]+)/$', api.PassGet.as_view()),
    url(r'^api/passes/update/(?P<pk>[0-9]+)/$', api.PassUpdate.as_view()),
    url(r'^api/passes/create/$', api.PassCreate.as_view()),

]
