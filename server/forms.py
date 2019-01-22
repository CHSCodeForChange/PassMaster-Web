from django import forms
from django.contrib.auth.models import User
from django_select2.forms import (
	Select2MultipleWidget,
	Select2Widget
)

from .models import *


class RequestPassForm(forms.Form):
	pass_type = forms.CharField(max_length=1, widget=forms.HiddenInput(), initial="1")

	destinationTeacher = forms.ModelChoiceField(
		queryset=Teacher.objects.all(),
		empty_label=None,
		required=False,
		widget=Select2Widget(
			attrs={'type': 'text',
			       'class': 'form-control',
				   'style': 'display: none;'}
		)
	)

	location = forms.CharField(max_length=12, required=False, widget=forms.TextInput(
		attrs={'type': 'text',
		       'class': 'form-control',
		       'style': 'display: none;'}))

	originTeacher = forms.ModelChoiceField(
		queryset=Teacher.objects.all(),
		empty_label=None,
		required=True,
		widget=Select2Widget(
			attrs={'type': 'text',
			       'class': 'form-control',
				   'style': 'display: none;'}
		)
	)

	date = forms.DateField(required=True, input_formats=['%Y-%m-%d'],
	                       initial=datetime.now, widget=forms.DateInput(
			attrs={'type': 'date',
			       'class': 'form-control'}))

	start = forms.TimeField(required=False, input_formats=['%H:%M'],
	                        widget=forms.TimeInput(
		                        attrs={'type': 'time',
		                               'class': 'form-control'}))
	end = forms.TimeField(required=False, input_formats=['%H:%M'],
	                      widget=forms.TimeInput(
		                      attrs={'type': 'time',
		                             'class': 'form-control'}))

	reason = forms.CharField(
		required=False,
		max_length=240,
		widget=forms.Textarea(
			attrs={
				'type': 'text',
				'class': 'form-control',
				'rows': '3',
			}
		)
	)

	session = forms.ChoiceField(required=False, choices=[(1, "First"), (2, "Second"), (3, "Both")],
	                            widget=forms.Select(
		                            attrs={'type': 'text',
		                                   'class': 'form-control',
		                                   'placeholder': 'Session',
		                                   'style': 'display: none;'}))

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
		elif self.cleaned_data['pass_type'] == '2':
			new_pass = LocationPass(approved=False, date=self.cleaned_data['date'],
			                        startTimeRequested=self.cleaned_data['start'],
			                        endTimeRequested=self.cleaned_data['end'], description=self.cleaned_data['reason'],
			                        student=student, location=self.cleaned_data['location'],
			                        originTeacher=self.cleaned_data['originTeacher'])
		elif self.cleaned_data['pass_type'] == '3':
			new_pass = SRTPass.create(approved=False, date=self.cleaned_data['date'],
			                          student=student, originTeacher=self.cleaned_data['originTeacher'],
			                          description=self.cleaned_data['reason'], destinationTeacher=self.cleaned_data['destinationTeacher'],
			                          session=self.cleaned_data['session'])
		else:
			print('This pass type cannot be created.')
			return
		new_pass.save()


# Teacher


class CreatePassForm(forms.Form):
	pass_type = forms.CharField(max_length=1, widget=forms.HiddenInput(), initial="1")

	originTeacher = forms.ModelChoiceField(
		queryset=Teacher.objects.all(),
		empty_label=None,
		widget=Select2Widget(
			attrs={'type': 'text',
				   'class': 'form-control'}
		)
	)

	destinationTeacher = forms.ModelChoiceField(
		queryset=Teacher.objects.all(),
		empty_label=None,
		required=False,
		widget=Select2Widget(
			attrs={'type': 'text',
				   'class': 'form-control'}
		)
	)

	location = forms.CharField(max_length=12, required=False, widget=forms.TextInput(
		attrs={'type': 'text',
		       'class': 'form-control'}))

	students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), required=True,
	                                          widget=Select2MultipleWidget(
		                                          attrs={'class': 'form-control',
		                                                 'placeholder': 'Reason for pass'}))

	date = forms.DateField(required=True, input_formats=['%Y-%m-%d'],
	                       initial=datetime.now, widget=forms.DateInput(
			attrs={'type': 'date',
			       'class': 'form-control'}))

	start = forms.TimeField(required=False, input_formats=['%H:%M'],
	                        widget=forms.TimeInput(
		                        attrs={'type': 'time',
		                               'class': 'form-control'}))
	end = forms.TimeField(required=False, input_formats=['%H:%M'],
	                      widget=forms.TimeInput(
		                      attrs={'type': 'time',
		                             'class': 'form-control'}))

	reason = forms.CharField(required=True, max_length=240, widget=forms.Textarea(
		attrs={'type': 'text',
		       'rows': '3',
		       'class': 'form-control'}))

	session = forms.ChoiceField(required=False, choices=[(1, "First"), (2, "Second"), (3, "Both")],
	                            widget=forms.Select(
		                            attrs={'type': 'text',
		                                   'class': 'form-control',
		                                   'placeholder': 'Session'}))

	# Yeah i know this is a terrible name, please find a new one
	specialDestination = forms.ModelChoiceField(
		queryset=Location.objects.all(),
		empty_label=None,
		required=False,
		widget=Select2Widget(
			attrs={'type': 'text',
				   'class': 'form-control'}
		)
	)

	initiatingTeacher = forms.ModelChoiceField(
		queryset=Teacher.objects.all(),
		empty_label=None,
		required=False,
		widget=Select2Widget(
			attrs={'type': 'text',
				   'class': 'form-control'}
		)
	)

	user = User()
	creator = Teacher()

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		self.creator = kwargs.pop('creator')
		super(CreatePassForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):

		if self.cleaned_data['pass_type'] == '1':
			for student in self.cleaned_data['students']:
				new_pass = TeacherPass(
					approved=True, date=self.cleaned_data['date'],
					startTimeRequested=self.cleaned_data['start'],
					endTimeRequested=self.cleaned_data['end'],
					description=self.cleaned_data['reason'],
					student=student, destinationTeacher=self.cleaned_data['destinationTeacher'],
					originTeacher=self.cleaned_data['originTeacher'],
					creator = self.creator
				)
				new_pass.save()
		elif self.cleaned_data['pass_type'] == '2':
			for student in self.cleaned_data['students']:
				new_pass = LocationPass(
					approved=True, date=self.cleaned_data['date'],
					startTimeRequested=self.cleaned_data['start'],
					endTimeRequested=self.cleaned_data['end'],
					description=self.cleaned_data['reason'],
					student=student, location=self.cleaned_data['location'],
					originTeacher=self.cleaned_data['originTeacher'],
					creator = self.creator
				)
				new_pass.save()
		elif self.cleaned_data['pass_type'] == '3':
			for student in self.cleaned_data['students']:
				new_pass = SRTPass.create(
					approved=True,
					date=self.cleaned_data['date'],
					student=student,
					originTeacher=self.cleaned_data['originTeacher'],
					description=self.cleaned_data['reason'],
					destinationTeacher=self.cleaned_data['destinationTeacher'],
					session=self.cleaned_data['session'],
					creator = self.creator
				)
				new_pass.save()
		elif self.cleaned_data['pass_type'] == '4':
			for student in self.cleaned_data['students']:
				new_pass = SpecialSRTPass.create(
					self.cleaned_data['date'],
					student=student,
					srtTeacher=self.cleaned_data['originTeacher'],
					description=self.cleaned_data['reason'],
					destination=self.cleaned_data['specialDestination'],
					session=self.cleaned_data['session'],
					initiatingTeacher=self.cleaned_data['initiatingTeacher'],
					creator = self.creator
				)
				new_pass.save()
