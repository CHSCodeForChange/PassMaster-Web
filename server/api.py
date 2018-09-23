from rest_framework import generics, authentication, permissions
from .models import *
from .serializers import *


class UserReadView(generics.RetrieveAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        user = self.request.GET.get("user")
        serializer_class = None

        if user is not None:
            user = User.objects.get(id=user)
            if user.profile.is_student():
                serializer_class = StudentSerializer
            elif user.profile.is_teacher():
                serializer_class = TeacherSerializer
        else:
            if self.request.user.profile.is_student():
                serializer_class = StudentSerializer

            elif self.request.user.profile.is_teacher():
                serializer_class = TeacherSerializer

        return serializer_class

    def get_object(self):
        user = self.request.GET.get("user")
        if user is not None:
            user = User.objects.get(id=user)
        else:
            user = self.request.user

        return user


class GenericPassReadView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = PassSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        type = self.request.GET.get("type")
        serializer_class = PassSerializer

        if type is not None:
            type = type.lower()
            if type == "teacher":
                serializer_class = TeacherPassSerializer
            elif type == "location":
                serializer_class = LocationPassSerializer
            elif type == "srt":
                serializer_class = SRTPassSerializer

        return serializer_class

    def get_queryset(self):
        return Pass.get_passes(self.request.user)

    def get_object(self):
        pk = self.kwargs.get("pk")
        user = self.request.user

        pass_object = Pass.get_passes(user).get(id=pk)
        pass_action = self.request.GET.get("action")

        if pass_action is not None and user.profile.is_teacher():
            pass_action = pass_action.lower()
            if pass_action == "approve":
                pass_object.approve(user.profile.teacher)
            elif pass_action == "signout":
                pass_object.leave(user.profile.teacher)
            elif pass_action == "signin":
                pass_object.arrive(user.profile.teacher)


        pass_type = self.request.GET.get("type")

        if pass_type is not None:
            pass_type = pass_type.lower()
            if pass_type == "teacher" or pass_type == "teacherpass":
                pass_object = pass_object.teacherpass
            elif pass_type == "location" or pass_type == "locationpass":
                pass_object = pass_object.locationpass
            elif pass_type == "srt" or pass_type == "srtpass":
                pass_object = pass_object.srtpass

        return pass_object



class PassListView(generics.ListAPIView):
    serializer_class = PassSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        passes = Pass.get_passes(self.request.user)

        query = self.request.GET.get("search")
        student = self.request.GET.get("student")
        originTeacher = self.request.GET.get("originTeacher")
        date = self.request.GET.get("date")
        approved = self.request.GET.get("approved")

        if query is not None:
            passes = passes.filter(description__icontains=query)

        elif student is not None:
            passes = passes.filter(student=student)

        elif originTeacher is not None:
            passes = passes.filter(originTeacher=originTeacher)

        elif date is not None:
            passes = passes.filter(date=date)

        elif approved is not None:
            passes = passes.filter(approved=approved)


        return passes


class PassCreateView(generics.CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        type = self.request.GET.get("type")

        serializer_class = None

        if type is not None:
            type = type.lower()
            if type == "teacher":
                serializer_class = TeacherPassSerializer
            elif type == "location":
                serializer_class = LocationPassSerializer
            elif type == "srt":
                serializer_class = SRTPassSerializer

        return serializer_class

    def perform_create(self, serializer):
        if self.request.user.profile.is_teacher():
            teacher = self.request.user.profile.teacher
            serializer.save().parent().approve(teacher) #TODO Fix bug where this does get approved but the api responds with the unapproved version

        elif self.request.user.profile.is_student():
            student = self.request.user.profile.student
            serializer.save(student=student)



