from django import forms
from django.contrib.auth.models import User
from django_select2.forms import Select2Widget
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
			       'placeholder': 'Destination Teacher'}
		)
	)

	location = forms.CharField(max_length=12, required=False, widget=forms.TextInput(
		attrs={'type': 'text',
		       'class': 'form-control',
		       'style': 'display: none;'}))

	originTeacher = forms.ModelChoiceField(
		queryset=Teacher.objects.all(),
		empty_label=None,
		widget=Select2Widget()
	)

	date = forms.DateField(required=True, input_formats=['%Y-%m-%d'],
	                       initial=datetime.now, widget=forms.DateInput(
			attrs={'type': 'date',
			       'class': 'form-control'}))

	start = forms.TimeField(input_formats=['%H:%M'],
	                        widget=forms.TimeInput(
		                        attrs={'type': 'time',
		                               'class': 'form-control'}))
	end = forms.TimeField(input_formats=['%H:%M'],
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

	originTeacher = forms.ModelChoiceField(
		queryset=Teacher.objects.all(),
		empty_label=None,
		widget=Select2Widget()
	)

	destinationTeacher = forms.ModelChoiceField(
		queryset=Teacher.objects.all(),
		empty_label=None,
		widget=Select2Widget()
	)

	location = forms.CharField(max_length=12, required=False, widget=forms.TextInput(
		attrs={'type': 'text',
		       'class': 'form-control',
		       'style': 'display: none;'}))

	students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), required=True,
	                                          widget=forms.SelectMultiple(
		                                          attrs={'class': 'form-control',
		                                                 'placeholder': 'Reason for pass'}))

	date = forms.DateField(required=True, input_formats=['%Y-%m-%d'],
	                       initial=datetime.now, widget=forms.DateInput(
			attrs={'type': 'date',
			       'class': 'form-control'}))

	start = forms.TimeField(input_formats=['%H:%M'],
	                        widget=forms.TimeInput(
		                        attrs={'type': 'time',
		                               'class': 'form-control'}))
	end = forms.TimeField(input_formats=['%H:%M'],
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
		                                   'placeholder': 'Session',
		                                   'style': 'display: none;'}))



	user = User()

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
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
					originTeacher=self.cleaned_data['originTeacher']
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
					originTeacher=self.cleaned_data['originTeacher']
				)
				new_pass.save()
		elif self.cleaned_data['pass_type'] == '3':
			for student in self.cleaned_data['students']:
				new_pass = SRTPass.create(
					self.cleaned_data['date'],
					student,
					self.cleaned_data['originTeacher'],
					self.cleaned_data['reason'],
					self.cleaned_data['destinationTeacher'],
					session=self.cleaned_data['session']
				)
				new_pass.save()
