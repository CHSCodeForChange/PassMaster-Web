from rest_framework import serializers

from .models import *


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

# Jared's serializers
#
# class PassSerializer(serializers.ModelSerializer):
#
#     originTeacher_name = serializers.CharField(source='originTeacher.__str__')
#     destinationTeacher_name = serializers.CharField(source='destinationTeacher.__str__')
#
#     class Meta:
#
#         model = Pass
#         fields = ('pk',
#                   'approved',
#                   'startTimeRequested',
#                   'endTimeRequested',
#                   'timeLeftOrigin',
#                   'timeArrivedDestination',
#                   'type',
#                   'student',
#                   'originTeacher',
#                   'originTeacher_name',
#                   'location',
#                   'destinationTeacher',
#                   'destinationTeacher_name',
#                   'description')
#
#
# class TeacherSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(source='__str__')
#
#     class Meta:
#
#         model = Teacher
#         fields = ('pk',
#                   'name',)
