from django.contrib.auth.models import User

from server.models import *


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

    def get_student(profile):
        return Student.objects.filter(profile=profile).first()

    def get_teacher(profile):
        return Teacher.objects.filter(profile=profile).first()

    def get_administrator(profile):
        return Administrator.objects.filter(profile=profile).first()

    def name(profile):
        return (profile.user.first_name + ' ' + profile.user.last_name)

    def __str__(self):
        return self.user.username
