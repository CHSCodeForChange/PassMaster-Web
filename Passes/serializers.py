from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        exclude = ()
        

