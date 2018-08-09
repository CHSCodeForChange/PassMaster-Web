from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import models
from datetime import datetime, timezone

from Passes.models import Pass

class NewPassForm(forms.Form):
    description = forms.CharField(label='Description', max_length=960, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control form'}))

    student = models.User()
    destinationTeacher = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, widget=forms.Select(
        attrs={'type': 'text',
               'class': 'form-control form'}))
    originTeacher = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, widget=forms.Select(
        attrs={'type': 'text',
               'class': 'form-control form'}))

    timeOfSession = forms.DateTimeField(widget=forms.Select(
        attrs={'type': 'text',
               'class': 'form-control form'}))

    timeOfRequest = datetime.now()

    session = forms.ChoiceField(label="",
                                initial='',
                                widget=forms.Select(),
                                required=True)


    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')
        super(NewPassForm, self).__init__(*args, **kwargs)
    def clean_description(self):
        description = self.cleaned_data['description']
        return description
    def clean_time(self):
        time = self.cleaned_data['timeOfSession']
        return time

    def save(self, commit=True):
        group = Group(
            description=self.cleaned_data['description'],
            destinationTeacher=destinationTeacher,
            originTeacher=originTeacher,
            timeOfSession=timeOfSession,
            timeOfRequest=timeOfRequest,
            )
        return pass
