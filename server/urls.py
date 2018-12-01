from django.conf.urls import url
from rest_framework.authtoken import views as auth_views

from . import views
from .api import *

rest = [
	url(r'^rest/login/$', auth_views.obtain_auth_token, name='login'),
	url(r'^rest/user/$', UserReadView.as_view(), name='user-read'),
	url(r'^rest/users/$', UserListView.as_view(), name='user-list'),
	url(r'^rest/students/$', StudentListView.as_view(), name='student-list'),
	url(r'^rest/teachers/$', TeacherListView.as_view(), name='teacher-list'),
	url(r'rest/passes/$', PassListView.as_view(), name='pass-list'),
	url(r'rest/passes/create/$', PassCreateView.as_view(), name='pass-create'),
	url(r'^rest/passes/(?P<pk>\d+)/$', GenericPassReadView.as_view(), name='pass-read'),
	url(r'^rest/passes/studenttop/$', StudentTopPassView.as_view(), name='student-top')
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

admin = [
	url(r'^admin_overview/$', views.admin_overview, name='admin_overview'),
	url(r'^admin_view/(?P<user_id>[0-9]+)/$', views.admin_view, name='admin_view'),
]

location = [
	url(r'^location/$', views.location_home, name='location_home')
]

urlpatterns = rest + student + teacher + location + admin