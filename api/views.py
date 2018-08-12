from rest_framework import viewsets
from .serializers import *
from Teacher.models import Teacher

# Create your views here.
class PassView(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer

    
class TeacherView(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        count = self.request.query_params.get('count', None)

        teachers = Teacher.objects.all()
        if name is not None:
            teachers = teachers.filter(profile__user__username__contains=name)
        if count is not None:
            teachers = teachers[:int(count)]

        return teachers