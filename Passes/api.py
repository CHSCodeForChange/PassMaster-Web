from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .serializers import *
from .models import *


class PassList(generics.ListAPIView):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    permission_classes = ()

    # def get_queryset(self):
    #     if self.request.user.profile.is_student():
    #         queryset = Pass.get_student_passes(self.request.user)
    #     elif self.request.user.profile.is_teacher():
    #         queryset = Pass.get_teacher_passes(self.request.user) 

    #     return queryset


class PassGet(generics.RetrieveAPIView):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    permission_classes = ()

class PassUpdate(generics.UpdateAPIView):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    permission_classes = ()


class PassCreate(generics.CreateAPIView):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    permission_classes = ()