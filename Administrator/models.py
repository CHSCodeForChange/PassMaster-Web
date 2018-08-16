from django.db import models


class Administrator (models.Model):
    profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)
