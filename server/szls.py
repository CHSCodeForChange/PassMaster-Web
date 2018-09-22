from rest_framework import serializers
from .models import *

class PassSerializer(serializers.ModelSerializer):
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
            'description'
        ]

        read_only_fields =