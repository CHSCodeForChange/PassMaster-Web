from dal import autocomplete

from django import forms
from django.contrib.auth.models import User

from .models import *


class TeacherPassForm(forms.ModelForm):
	originTeacher = forms.ModelChoiceField(
		queryset=Teacher.objects.all(),
		widget=autocomplete.ModelSelect2(url='/teacher/autocomplete')
	)

	class Meta:
		model = TeacherPass
		fields = ('__all__')


class RequestPassForm(forms.Form):
	pass_type = forms.CharField(max_length=1, widget=forms.HiddenInput(), initial="1")

	destinationTeacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label=None,
	                                            label="Destination teacher", required=False, )

	location = forms.CharField(max_length=12, required=False, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control',
               'placeholder': 'Location',
               'style': 'display: none;'}))

	originTeacher = forms.ModelChoiceField(
		queryset=Teacher.objects.all(),
		widget=autocomplete.ModelSelect2(url='/teacher/autocomplete')
	)

	date = forms.DateField(label='Date', required=True, input_formats=['%Y-%m-%d'],
	                       initial=datetime.now, widget=forms.DateInput(
			attrs={'type': 'date',
			       'class': 'form-control'}))

	start = forms.TimeField(label='Start time', required=True, input_formats=['%H:%M'],
	                        widget=forms.TimeInput(
		                        attrs={'type': 'time',
		                               'class': 'form-control'}))
	end = forms.TimeField(label='End time', required=True, input_formats=['%H:%M'],
	                      widget=forms.TimeInput(
		                      attrs={'type': 'time',
		                             'class': 'form-control'}))

	reason = forms.CharField(label='', required=True, max_length=240, widget=forms.TextInput(
        attrs={'type': 'text',
               'class': 'form-control',
               #    'rows': '3'
               'placeholder': 'Reason for pass'}))

	user = User()

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(RequestPassForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		student = Student.objects.get(profile=self.user.profile)
		if self.cleaned_data['pass_type'] == '1':
			new_pass = TeacherPass(approved=False, date=self.cleaned_data['date'],
			                       startTimeRequested=self.cleaned_data['start'],
			                       endTimeRequested=self.cleaned_data['end'], description=self.cleaned_data['reason'],
			                       student=student, destinationTeacher=self.cleaned_data['destinationTeacher'],
			                       originTeacher=self.cleaned_data['originTeacher'])
		else:
			new_pass = LocationPass(approved=False, date=self.cleaned_data['date'],
			                        startTimeRequested=self.cleaned_data['start'],
			                        endTimeRequested=self.cleaned_data['end'], description=self.cleaned_data['reason'],
			                        student=student, location=self.cleaned_data['location'],
			                        originTeacher=self.cleaned_data['originTeacher'])
		new_pass.save()


# Teacher


class CreatePassForm(forms.Form):
	pass_type = forms.CharField(max_length=1, widget=forms.HiddenInput(), initial="1")

	destinationTeacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label=None,
	                                            label="Destination teacher", required=False, )

	location = forms.CharField(max_length=12, required=False, widget=forms.TextInput(
		attrs={'type': 'text',
		       'class': 'form-control',
		       'placeholder': 'Location',
		       'style': 'display: none;'}))

	students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), label="Student(s)", required=True)

	date = forms.DateField(label='Date', required=True, input_formats=['%Y-%m-%d'],
	                       initial=datetime.now, widget=forms.DateInput(
			attrs={'type': 'date',
			       'class': 'form-control'}))

	start = forms.TimeField(label='Start time', required=True, input_formats=['%H:%M'],
	                        widget=forms.TimeInput(
		                        attrs={'type': 'time',
		                               'class': 'form-control'}))
	end = forms.TimeField(label='End time', required=True, input_formats=['%H:%M'],
	                      widget=forms.TimeInput(
		                      attrs={'type': 'time',
		                             'class': 'form-control'}))

	reason = forms.CharField(label='', required=True, max_length=240, widget=forms.TextInput(
		attrs={'type': 'text',
		       'class': 'form-control',
		       'placeholder': 'Reason for pass'}))

	user = User()

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(CreatePassForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		originTeacher = Teacher.objects.get(profile=self.user.profile)

		if self.cleaned_data['pass_type'] == '1':
			for student in self.cleaned_data['students']:
				new_pass = TeacherPass(approved=True, date=self.cleaned_data['date'],
				                       startTimeRequested=self.cleaned_data['start'],
				                       endTimeRequested=self.cleaned_data['end'],
				                       description=self.cleaned_data['reason'],
				                       student=student, destinationTeacher=self.cleaned_data['destinationTeacher'],
				                       originTeacher=originTeacher)
				new_pass.save()
		else:
			for student in self.cleaned_data['students']:
				new_pass = LocationPass(approved=True, date=self.cleaned_data['date'],
				                        startTimeRequested=self.cleaned_data['start'],
				                        endTimeRequested=self.cleaned_data['end'],
				                        description=self.cleaned_data['reason'],
				                        student=student, location=self.cleaned_data['location'],
				                        originTeacher=originTeacher)
				new_pass.save()
