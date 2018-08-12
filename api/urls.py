from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('passes', views.PassView)
router.register('teachers', views.TeacherView)
router.register('users', views.UserView)

urlpatterns = [
    url('', include(router.urls))
]