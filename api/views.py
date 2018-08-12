from django.shortcuts import render
from rest_framework import viewsets
from Passes.models import Pass
from .serializers import *
from Teacher.models import Teacher
from django.contrib.auth.models import User

# Create your views here.
class PassView(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer

    
class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        count = self.request.query_params.get('count', None)

        teachers = Teacher.objects.all()
        if name is not None:
            teachers = teachers.filter(profile__user__username__contains=name)
        if count is not None:
            teachers = teachers[:int(count)]

        return teachers


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = self.queryset.exclude(id=self.request.user.id)
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username__icontains=username)
        return queryset
    