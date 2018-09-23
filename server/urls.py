from django.conf.urls import url, include
from django.views.generic import RedirectView
from rest_framework.authtoken import views as drfviews
from . import api
from . import views

from rest_framework.documentation import include_docs_urls
from .rest import *
from rest_framework.authtoken import views as auth_views


rest = [
	url(r'^rest/login/$', auth_views.obtain_auth_token, name='login'),
	url(r'^rest/user/$', UserReadView.as_view(), name="user-read"),
	url(r'rest/passes/$', PassListView.as_view(), name='pass-list'),
	url(r'rest/passes/create/$', PassCreateView.as_view(), name='pass-create'),
	url(r'^rest/passes/(?P<pk>\d+)/$', GenericPassReadView.as_view(), name='pass-read')
]

api = [	
    url(r'^api/user/$', api.UserGet.as_view()),
	url(r'^api/passes/$', api.PassList.as_view()),
	url(r'^docs/', include('rest_framework_docs.urls')),
	url(r'^api/passes/(?P<pk>[0-9]+)/$', api.PassGet.as_view()),
    url(r'^api/passes/location/(?P<pk>[0-9]+)/$', api.LocationPassGet.as_view()),
    url(r'^api/passes/srt/(?P<pk>[0-9]+)/$', api.SRTPassGet.as_view()),
    url(r'^api/passes/teacher/(?P<pk>[0-9]+)/$', api.TeacherPassGet.as_view()),

	url(r'^api/api-token-auth/', drfviews.obtain_auth_token),

    url(r'^api/passes/update/(?P<pk>[0-9]+)/$', api.PassUpdate.as_view()),

    url(r'^api/passes/create/location/$', api.LocationPassCreate.as_view()),
    url(r'^api/passes/create/srt/$', api.SRTPassCreate.as_view()),
    url(r'^api/passes/create/teacher/$', api.TeacherPassCreate.as_view()),
]

student = [
	url(r'^student/$', views.student_home, name='student_home'),
]

teacher = [
	url(r'^teacher/approve/(?P<pass_id>[0-9]+)/$', views.approve, name='approve'),
	url(r'^teacher/checkout/(?P<pass_id>[0-9]+)/$', views.checkout, name='checkout'),
	url(r'^teacher/checkin/(?P<pass_id>[0-9]+)/$', views.checkin, name='checkin'),

	url(r'^teacher/$', views.teacher_home, name='teacher_home'),
]

location = [
	url(r'^location/$', views.location_home, name='location_home')
]

urlpatterns = rest + api + student + teacher + location