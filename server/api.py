from rest_framework import generics, authentication, permissions

from .serializers import *


class UserReadView(generics.RetrieveAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        user = self.request.GET.get("user")
        if user is not None:
            user = User.objects.get(id=user)
        else:
            user = self.request.user

        if user.profile.member_type == '1':
            return StudentSerializer
        elif user.profile.member_type == '2':
            return TeacherSerializer
        else:
            return UserSerializer


    def get_object(self):
        user = self.request.GET.get("user")
        if user is not None:
            user = User.objects.get(id=user)
        else:
            user = self.request.user

        if user.profile.member_type == '1':
            return user.profile.student
        elif user.profile.member_type == '2':
            return user.profile.teacher
        else:
            return user


class UserListView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.GET.get("username")
        type = self.request.GET.get("type")
        queryset = User.objects.all()
        if type is not None:
            queryset = queryset.filter(profile__member_type=type)
        if username is not None:
            queryset = queryset.filter(username__icontains=username) | queryset.filter(first_name__icontains=username) | queryset.filter(last_name__icontains=username)

        return queryset


class StudentListView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StudentSerializer

    def get_queryset(self):
        username = self.request.GET.get("username")
        queryset = Student.objects.all()

        if username is not None:
            queryset = queryset.filter(profile__user__username__icontains=username) | queryset.filter(profile__user__last_name__icontains=username) | queryset.filter(profile__user__first_name__icontains=username)

        return queryset


class TeacherListView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TeacherSerializer

    def get_queryset(self):
        username = self.request.GET.get("username")
        queryset = Teacher.objects.all()

        if username is not None:
            queryset = queryset.filter(profile__user__username__icontains=username) | queryset.filter(profile__user__last_name__icontains=username) | queryset.filter(profile__user__first_name__icontains=username)

        return queryset


class GenericPassReadView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = PassSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        pass_type = self.request.GET.get("type")
        serializer_class = PassSerializer

        if pass_type is not None:
            pass_type = pass_type.lower()
            if pass_type == "teacher" or pass_type == "teacherpass":
                serializer_class = TeacherPassSerializer
            elif pass_type == "location" or pass_type == "locationpass":
                serializer_class = LocationPassSerializer
            elif pass_type == "srt" or pass_type == "srtpass":
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
                pass_object.sign_out(user.profile.teacher)
            elif pass_action == "signin":
                pass_object.sign_in(user.profile.teacher)

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
        user = self.request.user
        passes = Pass.get_passes(user)

        list = self.request.GET.get("list")
        passtype = self.request.GET.get("passtype")
        query = self.request.GET.get("search")
        student = self.request.GET.get("student")
        originTeacher = self.request.GET.get("originTeacher")
        date = self.request.GET.get("date")
        approved = self.request.GET.get("approved")

        if list is not None:
            list = list.lower()
            if list == 'active':
                passes = Pass.get_students_active_passes(user)
            elif list == 'pending':
                passes = Pass.get_students_pending_passes(user)
            elif list =='student-old' or list == 'student old':
                passes = Pass.get_students_old_passes(user)

            elif list == 'teacher-pending' or list == 'teacher pending':
                passes = Pass.get_teachers_unapproved_passes(user)

            elif list == 'teacher-incoming' or list == 'teacher incoming':
                passes = Pass.get_teachers_incoming_student_passes(user)

            elif list == 'teacher-outgoing' or list == 'teacher outgoing':
                passes = Pass.get_teachers_outgoing_student_passes(user)

            elif list == 'teacher-old' or list == 'teacher old':
                passes = Pass.get_teachers_old_passes(user)

        elif query is not None:
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
            if type == "teacher" or type == 'teacherpass':
                serializer_class = TeacherPassSerializer
            elif type == "location" or type == 'locationpass':
                serializer_class = LocationPassSerializer
            elif type == "srt" or type == 'srtpass':
                serializer_class = SRTPassSerializer

        return serializer_class

    def perform_create(self, serializer):
        if self.request.user.profile.is_teacher():
            teacher = self.request.user.profile.teacher
            _pass = serializer.save().parent().approve(teacher) #TODO Fix bug where this does get approved but the api responds with the unapproved version

        elif self.request.user.profile.is_student():
            student = self.request.user.profile.student
            _pass = serializer.save(student=student)

        type = self.request.GET.get("type")

        if _pass is not None (type == "srt" or type == "srtpass"):
            _pass.srtpass.fill_time()




