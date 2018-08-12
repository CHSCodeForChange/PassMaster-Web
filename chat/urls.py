from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UserView)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', views.home),
    url(r'^new/$', views.new),
    url(r'^new/(?P<user_id>[0-9]+)/$', views.create_conversation),
    url(r'^(?P<conversation_id>[0-9]+)/', views.conversation),
]
