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
    student = StudentSerializer()
    originTeacher = TeacherSerializer()
    destinationTeacher = TeacherSerializer()

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

            'description',
        )

        read_only_fields = (
            'pk',
            'approved',
            'timeLeftOrigin',
            'timeArrivedDestination',
        )

class LocationPassSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    originTeacher = TeacherSerializer()
    destinationTeacher = TeacherSerializer()

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
            'location',

            'description'
        )

        read_only_fields = (
            'pk',
            'approved',
            'timeLeftOrigin',
            'timeArrivedDestination',
        )

class SRTPassSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    originTeacher = TeacherSerializer()
    destinationTeacher = TeacherSerializer()

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
            'timeArrivedOrigin'

            'student',
            'originTeacher',
            'destinationTeacher',

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