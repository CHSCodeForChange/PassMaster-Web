from django.db import models


class Teacher (models.Model):
    profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)
    idName = models.CharField(max_length=250, default='stuff')

    def __str__(self):
        return self.profile.user.username

    def get_students(self):
        pass
