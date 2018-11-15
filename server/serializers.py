from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class StudentSerializer(serializers.ModelSerializer):
    user_pk = serializers.CharField(source='profile.user.pk')
    username = serializers.CharField(source='profile.user.username')
    first_name = serializers.CharField(source='profile.user.first_name')
    last_name = serializers.CharField(source='profile.user.last_name')
    email = serializers.CharField(source='profile.user.email')
    type = serializers.CharField(source='profile.member_type')

    class Meta:
        model = Student
        fields = [
            'user_pk',
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'type',
        ]


class TeacherSerializer(serializers.ModelSerializer):
    user_pk = serializers.CharField(source='profile.user.pk')
    username = serializers.CharField(source='profile.user.username')
    first_name = serializers.CharField(source='profile.user.first_name')
    last_name = serializers.CharField(source='profile.user.last_name')
    email = serializers.CharField(source='profile.user.email')
    type = serializers.CharField(source='profile.member_type')

    class Meta:
        model = Teacher
        fields = [
            'user_pk',
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'type',
        ]


class UserSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='profile.member_type')

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'type',
        ]


class PassSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='pass_type')
    destination = serializers.CharField(source='get_destination')

    can_approve = serializers.SerializerMethodField(read_only=True)
    can_sign_in = serializers.SerializerMethodField(read_only=True)
    can_sign_out = serializers.SerializerMethodField(read_only=True)

    student_info = serializers.SerializerMethodField(read_only=True)
    originTeacher_info = serializers.SerializerMethodField(read_only=True)

    def get_student_info(self, obj):
        student = obj.student
        serializer = StudentSerializer(student)
        return serializer.data

    def get_originTeacher_info(self, obj):
        originTeacher = obj.originTeacher
        serializer = StudentSerializer(originTeacher)
        return serializer.data

    def get_can_approve(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_approve(profile.teacher)

    def get_can_sign_in(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_sign_in(profile.teacher)

    def get_can_sign_out(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_sign_out(profile.teacher)

    class Meta:
        model = Pass
        fields = [
            'pk',
            'approved',

            'date',
            'startTimeRequested',
            'endTimeRequested',

            'timeLeftOrigin',
            'timeArrivedDestination',

            'student',
            'originTeacher',

            'student_info',
            'originTeacher_info',

            'description',

            'type',
            'destination',

            'can_approve',
            'can_sign_in',
            'can_sign_out'
        ]


class TeacherPassSerializer(serializers.ModelSerializer):
    student_info = serializers.SerializerMethodField(read_only=True)
    originTeacher_info = serializers.SerializerMethodField(read_only=True)
    destinationTeacher_info = serializers.SerializerMethodField(read_only=True)

    can_approve = serializers.SerializerMethodField(read_only=True)
    can_sign_in = serializers.SerializerMethodField(read_only=True)
    can_sign_out = serializers.SerializerMethodField(read_only=True)

    def get_student_info(self, obj):
        student = obj.student
        serializer = StudentSerializer(student)
        return serializer.data

    def get_originTeacher_info(self, obj):
        originTeacher = obj.originTeacher
        serializer = StudentSerializer(originTeacher)
        return serializer.data

    def get_destinationTeacher_info(self, obj):
        destinationTeacher = obj.destinationTeacher
        serializer = StudentSerializer(destinationTeacher)
        return serializer.data

    def get_can_approve(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_approve(profile.teacher)

    def get_can_sign_in(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_sign_in(profile.teacher)

    def get_can_sign_out(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_sign_out(profile.teacher)

    class Meta:
        model = TeacherPass
        fields = (
            'pk',
            'approved',

            'date',
            'startTimeRequested',
            'endTimeRequested',

            'timeLeftOrigin',
            'timeArrivedDestination',

            'student',
            'originTeacher',
            'destinationTeacher',
            'student_info',
            'originTeacher_info',
            'destinationTeacher_info',

            'description',

            'can_approve',
            'can_sign_in',
            'can_sign_out'
        )

        read_only_fields = (
            'pk',
            'approved',
            'timeLeftOrigin',
            'timeArrivedDestination',

            'can_approve',
            'can_sign_in',
            'can_sign_out'
        )


class LocationPassSerializer(serializers.ModelSerializer):
    student_info = serializers.SerializerMethodField(read_only=True)
    originTeacher_info = serializers.SerializerMethodField(read_only=True)

    can_approve = serializers.SerializerMethodField(read_only=True)
    can_sign_in = serializers.SerializerMethodField(read_only=True)
    can_sign_out = serializers.SerializerMethodField(read_only=True)

    def get_student_info(self, obj):
        student = obj.student
        serializer = StudentSerializer(student)
        return serializer.data

    def get_originTeacher_info(self, obj):
        originTeacher = obj.originTeacher
        serializer = StudentSerializer(originTeacher)
        return serializer.data

    def get_can_approve(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_approve(profile.teacher)

    def get_can_sign_in(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_sign_in(profile.teacher)

    def get_can_sign_out(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_sign_out(profile.teacher)


    class Meta:
        model = LocationPass
        fields = (
            'pk',
            'approved',

            'date',
            'startTimeRequested',
            'endTimeRequested',

            'timeLeftOrigin',
            'timeArrivedDestination',

            'student',
            'originTeacher',
            'student_info',
            'originTeacher_info',

            'location',

            'description',

            'can_approve',
            'can_sign_in',
            'can_sign_out'
        )

        read_only_fields = (
            'pk',
            'approved',
            'timeLeftOrigin',
            'timeArrivedDestination',

            'can_approve',
            'can_sign_in',
            'can_sign_out'
        )



class SRTPassSerializer(serializers.ModelSerializer):
    student_info = serializers.SerializerMethodField(read_only=True)
    originTeacher_info = serializers.SerializerMethodField(read_only=True)
    destinationTeacher_info = serializers.SerializerMethodField(read_only=True)

    can_approve = serializers.SerializerMethodField(read_only=True)
    can_sign_in = serializers.SerializerMethodField(read_only=True)
    can_sign_out = serializers.SerializerMethodField(read_only=True)

    def get_student_info(self, obj):
        student = obj.student
        serializer = StudentSerializer(student)
        return serializer.data

    def get_originTeacher_info(self, obj):
        originTeacher = obj.originTeacher
        serializer = StudentSerializer(originTeacher)
        return serializer.data

    def get_destinationTeacher_info(self, obj):
        destinationTeacher = obj.destinationTeacher
        serializer = StudentSerializer(destinationTeacher)
        return serializer.data

    def get_can_approve(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_approve(profile.teacher)

    def get_can_sign_in(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_sign_in(profile.teacher)

    def get_can_sign_out(self, obj):
        profile = self.context.get('request').user.profile
        if not profile.is_teacher():
            return False
        return obj.can_sign_out(profile.teacher)

    class Meta:
        model = SRTPass
        fields = (
            'pk',
            'approved',

            'date',
            'session',

            'timeLeftOrigin',
            'timeArrivedDestination',
            'timeLeftDestination',
            'timeArrivedOrigin',

            'student',
            'originTeacher',
            'destinationTeacher',
            'student_info',
            'originTeacher_info',
            'destinationTeacher_info',

            'description',

            'can_approve',
            'can_sign_in',
            'can_sign_out'
        )

        read_only_fields = (
            'pk',
            'approved',
            'timeLeftOrigin',
            'timeArrivedDestination',
            'timeLeftDestination',
            'TimeArrivedOrigin',

            'can_approve',
            'can_sign_in',
            'can_sign_out'
        )