from django.shortcuts import render
from rest_framework import viewsets
from Passes.models import Pass
from .serializers import *
from Teacher.models import Teacher

# Create your views here.
class PassView(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer

    
class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        if name is not None:
            return Teacher.objects.filter(profile__user__username__contains=name)
        else: 
            return Teacher.objects.all()