from django.conf.urls import url
from django.views.generic import RedirectView

from server.autocomp import TeacherAutocomplete
from . import api
from . import views

urlpatterns = [
	# API
    url(r'^api/passes/$', api.PassList.as_view()),

    url(r'^api/passes/(?P<pk>[0-9]+)/$', api.PassGet.as_view()),
    url(r'^api/passes/location/(?P<pk>[0-9]+)/$', api.LocationPassGet.as_view()),
    url(r'^api/passes/srt/(?P<pk>[0-9]+)/$', api.SRTPassGet.as_view()),
    url(r'^api/passes/teacher/(?P<pk>[0-9]+)/$', api.TeacherPassGet.as_view()),

    url(r'^api/passes/update/(?P<pk>[0-9]+)/$', api.PassUpdate.as_view()),

    url(r'^api/passes/create/location/$', api.LocationPassCreate.as_view()),
    url(r'^api/passes/create/srt/$', api.SRTPassCreate.as_view()),
    url(r'^api/passes/create/teacher/$', api.TeacherPassCreate.as_view()),

	# Student
	url(r'^student/request/', views.requestPass),
	url(r'^student/requestTeacherPass/', views.requestTeacherPass),
	url(r'^student/$', views.student_home, name='student_home'),
	url(r'^student/', RedirectView.as_view(pattern_name='student_home', permanent=False)),

	# Teacher
	url(r'^teacher/approve/(?P<pass_id>[0-9]+)/$', views.approve, name='approve'),
	url(r'^teacher/checkout/(?P<pass_id>[0-9]+)/$', views.checkout, name='checkout'),
	url(r'^teacher/checkin/(?P<pass_id>[0-9]+)/$', views.checkin, name='checkin'),
	url(
		r'^teacher/autocomplete/$',
		TeacherAutocomplete.as_view(),
		name='teacher-autocomplete',
	),
	url(r'^teacher/$', views.teacher_home, name='teacher_home'),
	url(r'^teacher/', RedirectView.as_view(pattern_name='teacher_home', permanent=False)),

]
