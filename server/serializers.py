from rest_framework import serializers

from .models import *
from accounts.models import Profile

class UserSerializer(serializers.ModelSerializer):
    first = serializers.CharField(source='user.first_name')
    last = serializers.CharField(source='user.last_name')
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Profile
        fields = ('pk',
                  'member_type',
                  'user',
                  'first',
                  'last',
                  'username',
                  'email')



class Read_PassSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='pass_type')

    class Meta:
        model = Pass
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
                    'type')

class Read_LocationPassSerializer(serializers.ModelSerializer):
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

class Read_SRTPassSerializer(serializers.ModelSerializer):
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

class Read_TeacherPassSerializer(serializers.ModelSerializer):
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
                    'description',
                    'destinationTeacher')

class StudentCreate_LocationPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationPass
        fields = ('date',
                    'startTimeRequested',
                    'endTimeRequested',
                    'originTeacher',
                    'description',
                    'location')

class TeacherCreate_LocationPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationPass
        fields = ('date',
                    'startTimeRequested',
                    'endTimeRequested',
                    'student',
                    'description',
                    'location')

class StudentCreate_SRTPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SRTPass
        fields = ('date',
                    'startTimeRequested',
                    'endTimeRequested',
                    'student',
                    'originTeacher',
                    'description',
                    'session',
                    'destinationTeacher')

class StudentCreate_TeacherPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherPass
        fields = ('date',
                    'startTimeRequested',
                    'endTimeRequested',
                    # 'student',
                    'originTeacher',
                    'description',
                    'destinationTeacher')


class TeacherCreate_TeacherPassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherPass
        fields = ('date',
                    'startTimeRequested',
                    'endTimeRequested',
                    'student',
                    'originTeacher',
                    'description',
                    'destinationTeacher')
