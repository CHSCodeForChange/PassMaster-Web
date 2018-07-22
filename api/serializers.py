from rest_framework import serializers
from Passes.models import Pass




class PassSerializer(serializers.ModelSerializer):

    originTeacher_name = serializers.CharField(source='originTeacher.__str__')
    destinationTeacher_name = serializers.CharField(source='destinationTeacher.__str__')

    class Meta:

        model = Pass
        fields = ('approved',
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
