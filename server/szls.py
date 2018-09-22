from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.__str__')
    type = serializers.CharField(source='profile.member_type')

    class Meta:
        model = User
        fields = [
            'pk',
            'username',
            'first_name',
            'last_name',
            'email',
            'token',
            'type'
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
    type = serializers.CharField(source='pass_type')

    class Meta:
        model = TeacherPass
        fields = ('pk',
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
                    'type')

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