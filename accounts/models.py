from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    # The manager to get Profile objects
    objects = models.Manager()

    # the one to one relationship with the user, as the profile class builds off of django's built in user class
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # the main timezone for this user
    timezone = models.CharField(max_length=50, default='EST')

    # defines which type of member the user/profile belongs to
    CHOICES = (('1', 'Student',), ('2', 'Teacher',), ('3', 'Administrator'))
    member_type = models.CharField(max_length=50, choices=CHOICES)



    def is_student(profile):
        return profile.member_type == '1'

    def is_teacher(profile):
        return profile.member_type == '2'

    def is_administrator(profile):
        return profile.member_type == '3'

    def name(profile):
        return (profile.user.first_name + ' ' + profile.user.last_name)
