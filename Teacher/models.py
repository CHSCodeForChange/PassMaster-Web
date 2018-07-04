from django.db import models
from accounts.models import Profile
# Create your models here.
class Teacher (models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


    def get_students(self):
        pass
