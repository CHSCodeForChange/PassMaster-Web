from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .serializers import *
from .models import *


class PassList(generics.ListAPIView):
    queryset = Pass.objects.all()
    serializer_class = Read_PassSerializer
    permission_classes = ()

    # def get_queryset(self):
    #     if self.request.user.profile.is_student():
    #         queryset = Pass.get_student_passes(self.request.user)
    #     elif self.request.user.profile.is_teacher():
    #         queryset = Pass.get_teacher_passes(self.request.user) 

    #     return queryset


class PassGet(generics.RetrieveAPIView):
    queryset = Pass.objects.all()
    serializer_class = Read_PassSerializer
    permission_classes = ()

class PassUpdate(generics.UpdateAPIView):
    queryset = Pass.objects.all()
    serializer_class = StudentCreate_LocationPassSerializer
    permission_classes = ()



class LocationPassCreate(generics.CreateAPIView):
    permission_classes = ()

    def get_serializer_class(self):
        if (self.request.user.profile.is_teacher()):
            return TeacherCreate_LocationPassSerializer
        else: 
            return StudentCreate_LocationPassSerializer

    def perform_create(self, serializer):
        if (self.request.user.profile.is_teacher()):
            new_pass = serializer.save(approved=True, originTeacher=self.request.user.profile.teacher)
        else: 
            serializer.save(student=self.request.user.profile.student)


class SRTPassCreate(generics.CreateAPIView):
    serializer_class = StudentCreate_SRTPassSerializer
    permission_classes = ()

class TeacherPassCreate(generics.CreateAPIView):
    permission_classes = ()

    def get_serializer_class(self):
        if (self.request.user.profile.is_teacher()):
            return TeacherCreate_TeacherPassSerializer
        else: 
            return StudentCreate_TeacherPassSerializer

    def perform_create(self, serializer):
        if (self.request.user.profile.is_teacher()):
            new_pass = serializer.save(approved=True)
            if (new_pass.destinationTeacher == self.request.user.profile.teacher):
                new_pass.approved = True
                new_pass.save()
        else: 
            serializer.save(student=self.request.user.profile.student)
