from django.db import models
from accounts.models import Profile
# Create your models here.
class Administrator (models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
