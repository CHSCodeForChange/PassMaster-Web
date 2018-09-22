from rest_framework import generics
from .models import *
from .szls import *

class PassReadView(generics.RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = PassSerializer
    authentication_classes = ()
    permission_classes = ()

    def get_queryset(self):
        return Pass.objects.all()

class PassListCreateView(generics.ListCreateAPIView):
    serializer_class = PassSerializer


