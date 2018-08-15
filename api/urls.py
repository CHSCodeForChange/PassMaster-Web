from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login_api/', views.post),
    url(r'^model_request/', views.model_request),
    url(r'^model_update/', views.model_update),
]