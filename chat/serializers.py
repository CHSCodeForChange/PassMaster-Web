from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk',
                  'username',)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('pk',
                  'conversation',
                  'sender',
                  'datetime',
                  'message',)