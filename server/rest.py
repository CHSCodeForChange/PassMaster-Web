from rest_framework import generics, authentication, permissions
from .models import *
from .szls import *


class UserReadView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


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
        pass_object = Pass.get_passes(self.request.user).get(id=pk)

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




