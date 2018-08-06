from rest_framework import serializers
from Passes.models import Pass
from Teacher.models import Teacher



class PassSerializer(serializers.ModelSerializer):

    originTeacher_name = serializers.CharField(source='originTeacher.__str__')
    destinationTeacher_name = serializers.CharField(source='destinationTeacher.__str__')

    class Meta:

        model = Pass
        fields = ('pk', 
                  'approved',
                  'startTimeRequested',
                  'endTimeRequested',
                  'timeLeftOrigin',
                  'timeArrivedDestination',
                  'type',
                  'student',
                  'originTeacher',
                  'originTeacher_name',
                  'location',
                  'destinationTeacher',
                  'destinationTeacher_name',
                  'description')


class TeacherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='__str__')

    class Meta:

        model = Teacher
        fields = ('pk', 
                  'name',)