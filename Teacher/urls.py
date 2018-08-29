from django.conf.urls import url
from . import views
from .autocomp import TeacherAutocomplete

urlpatterns = [
    url(r'^$', views.home),
    url(r'^approve/(?P<pass_id>[0-9]+)/$', views.approve, name='approve'),
    url(r'^checkout/(?P<pass_id>[0-9]+)/$', views.checkout, name='checkout'), 
    url(r'^checkin/(?P<pass_id>[0-9]+)/$', views.checkin, name='checkin'),
    url(
        r'^autocomplete/$',
        TeacherAutocomplete.as_view(),
        name='teacher-autocomplete',
    ),
]
