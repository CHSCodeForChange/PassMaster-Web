from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import models
from datetime import datetime, timezone
from Student.models import Student
from Passes.models import Pass
from django.contrib.auth.models import User
from Teacher.models import Teacher


class RequestForm(forms.Form):
    destinationTeacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label=None)
    originTeacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label=None)

    start = forms.DateTimeField(label='Start time', input_formats=['%Y-%m-%dT%H:%M'],
                                widget=forms.DateTimeInput(
                                    attrs={'type': 'datetime-local',
                                           'class': 'form-control'}))
    end = forms.DateTimeField(label='End time', input_formats=['%Y-%m-%dT%H:%M'],
                              widget=forms.DateTimeInput(
                                  attrs={'type': 'datetime-local',
                                         'class': 'form-control'}))

    reason = forms.CharField(label='', required=True, max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control',
               'placeholder': 'Why'}))

    user = models.User()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(RequestForm, self).__init__(*args, **kwargs)

    def clean_sending(self):
        b = self.cleaned_data['sending']

        if Teacher.objects.filter(idName=b).exists():
            return b
        else:
            raise ValidationError('orgin teacher is invalid')

    def clean_location(self):
        b = self.cleaned_data['location']

        if Teacher.objects.filter(idName=b).exists():
            return b
        else:
            raise ValidationError('recieving teacher is invalid')
    def save(self, commit=True):
        print(self.user)
        student = Student.objects.get(profile=self.user.profile)

        newPass = Pass(type='1', approved=False, startTimeRequested=self.cleaned_data['start'],
                       endTimeRequested=self.cleaned_data['end'], description=self.cleaned_data['reason'],
                       student=student, destinationTeacher=self.cleaned_data['destinationTeacher'],
                       originTeacher=self.cleaned_data['originTeacher'])
        return newPass
