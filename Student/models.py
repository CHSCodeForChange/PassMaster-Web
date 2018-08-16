from django.db import models
from Teacher.models import Teacher


class Student (models.Model):
    profile = models.OneToOneField('accounts.Profile', on_delete=models.CASCADE)

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
