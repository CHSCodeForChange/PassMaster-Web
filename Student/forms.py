from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import models
from datetime import datetime, timezone
from Student.models import Student
from Passes.models import Pass


class RequestForm(forms.Form):
    location = forms.CharField(label='', required=True, max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control',
               'placeholder': 'Location'}))
    start = forms.DateTimeField(label='Start time', input_formats=['%Y-%m-%dT%H:%M'],
                                widget=forms.DateTimeInput(
                                    attrs={'type': 'datetime-local',
                                           'class': 'form-control'}))
    end = forms.DateTimeField(label='End time', input_formats=['%Y-%m-%dT%H:%M'],
                              widget=forms.DateTimeInput(
                                  attrs={'type': 'datetime-local',
                                         'class': 'form-control'}))
    user = models.User()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RequestForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        print('student is ', self.user, self.user.profile)
        student = Student.objects.get(profile=self.user.profile)
        newPass = Pass(approved=False, startTimeRequested=self.cleaned_data['start'], endTimeRequested=self.cleaned_data['end'],
                       student=student, originTeacher=student.defaultOrgin)
        return newPass
