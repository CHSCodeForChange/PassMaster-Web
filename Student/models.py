from django.db import models
from accounts.models import Profile
from Teacher.models import Teacher
# Create your models here.
class Student (models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    teachers = models.ManyToManyField(Teacher, related_name="teacher_list")

    defaultOrgin = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="srt_teacher"
    )

    def __str__(self):
        return self.profile.user.username

    def get_deforgin(self):
        return self.defaultOrgin
