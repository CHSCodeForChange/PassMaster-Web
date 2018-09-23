from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class StudentSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='profile.member_type')
    student = serializers.CharField(source='profile.student.pk')

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'type',
            'student'
        ]


class TeacherSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='profile.member_type')
    teacher = serializers.CharField(source='profile.teacher.pk')

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'type',
            'teacher'
        ]

class PassSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='pass_type')

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
            'type'
        ]


class TeacherPassSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = LocationPass
        fields = ('pk',
                    'approved',
                    'date',
                    'startTimeRequested',
                    'endTimeRequested',
                    'timeLeftOrigin',
                    'timeArrivedDestination',
                    'student',
                    'originTeacher',
                    'description',
                    'location')

        read_only_fields = (
            'pk',
            'approved',
            'timeLeftOrigin',
            'timeArrivedDestination',
        )

class SRTPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SRTPass
        fields = ('pk',
                    'approved',
                    'date',
                    'startTimeRequested',
                    'endTimeRequested',
                    'timeLeftOrigin',
                    'timeArrivedDestination',
                    'student',
                    'originTeacher',
                    'description',
                    'destinationTeacher',
                    'session',
                    'timeLeftDestination',
                    'timeArrivedOrigin')

        read_only_fields = (
            'pk',
            'approved',
            'timeLeftOrigin',
            'timeArrivedDestination',
            'timeLeftDestination',
            'TimeArrivedOrigin'
        )