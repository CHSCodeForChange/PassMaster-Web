from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class StudentSerializer(serializers.ModelSerializer):
    pk = serializers.CharField(source='profile.user.pk')
    username = serializers.CharField(source='profile.user.username')
    first_name = serializers.CharField(source='profile.user.first_name')
    last_name = serializers.CharField(source='profile.user.last_name')
    email = serializers.CharField(source='profile.user.email')
    type = serializers.CharField(source='profile.member_type')

    class Meta:
        model = Student
        fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'type',
        ]


class TeacherSerializer(serializers.ModelSerializer):
    pk = serializers.CharField(source='profile.user.pk')
    username = serializers.CharField(source='profile.user.username')
    first_name = serializers.CharField(source='profile.user.first_name')
    last_name = serializers.CharField(source='profile.user.last_name')
    email = serializers.CharField(source='profile.user.email')
    type = serializers.CharField(source='profile.member_type')

    class Meta:
        model = Teacher
        fields = [
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

    student = StudentSerializer()
    originTeacher = TeacherSerializer()

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

            'description',

            'type',
            'destination'
        ]


class TeacherPassSerializer(serializers.ModelSerializer):
    student_info = serializers.SerializerMethodField(read_only=True)
    originTeacher_info = serializers.SerializerMethodField(read_only=True)
    destinationTeacher_info = serializers.SerializerMethodField(read_only=True)

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
            'student_info',
            'originTeacher',
            'originTeacher_info',
            'destinationTeacher',
            'destinationTeacher_info',

            'description',
        )

        read_only_fields = (
            'pk',
            'approved',
            'timeLeftOrigin',
            'timeArrivedDestination',
        )

    def get_student_info(self, obj):
        student = obj.student
        serializer = StudentSerializer(student)
        return serializer.data

    def get_originTeacher_info(self, obj):
        originTeacher = obj.originTeacher
        serializer = TeacherSerializer(originTeacher)
        return serializer.data

    def get_destinationTeacher_info(self, obj):
        destinationTeacher = obj.destinationTeacher
        serializer = TeacherSerializer(destinationTeacher)
        return serializer.data


class LocationPassSerializer(serializers.ModelSerializer):
    student_info = serializers.SerializerMethodField(read_only=True)
    originTeacher_info = serializers.SerializerMethodField(read_only=True)


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
            'student_info',
            'originTeacher',
            'originTeacher_info',
            'location',

            'description'
        )

        read_only_fields = (
            'pk',
            'approved',
            'timeLeftOrigin',
            'timeArrivedDestination',
        )

    def get_student_info(self, obj):
        student = obj.student
        serializer = StudentSerializer(student)
        return serializer.data

    def get_originTeacher_info(self, obj):
        originTeacher = obj.originTeacher
        serializer = TeacherSerializer(originTeacher)
        return serializer.data


class SRTPassSerializer(serializers.ModelSerializer):
    student_info = serializers.SerializerMethodField(read_only=True)
    originTeacher_info = serializers.SerializerMethodField(read_only=True)
    destinationTeacher_info = serializers.SerializerMethodField(read_only=True)

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
            'student_info',
            'originTeacher',
            'originTeacher_info',
            'destinationTeacher',
            'destinationTeacher_info',
 
            'description',
        )

        read_only_fields = (
            'pk',
            'approved',
            'timeLeftOrigin',
            'timeArrivedDestination',
            'timeLeftDestination',
            'TimeArrivedOrigin'
        )

        def get_student_info(self, obj):
            student = obj.student
            serializer = StudentSerializer(student)
            return serializer.data

        def get_originTeacher_info(self, obj):
            originTeacher = obj.originTeacher
            serializer = TeacherSerializer(originTeacher)
            return serializer.data

        def get_destinationTeacher_info(self, obj):
            destinationTeacher = obj.destinationTeacher
            serializer = TeacherSerializer(destinationTeacher)
            return serializer.data