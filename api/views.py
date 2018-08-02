from django.shortcuts import render
from rest_framework import viewsets
from Passes.models import Pass
from .serializers import PassSerializer

# Create your views here.
class PassView(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer