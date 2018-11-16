import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import models
from .forms import *


@login_required
def admin_overview(request):
	if not request.user.is_authenticated():
		return redirect('/login')
	if not request.user.profile.is_administrator():
		return redirect('/')

	students = Student.objects.all()

	for i in students:
		i.number_pass = len(Pass.objects.filter(student=i))

	print(students[0].profile.user.first_name)
	return render(request, "administrator/admin_overview.html",
	              {'students': students})


@login_required
def admin_view(request, user_id):
	if not request.user.is_authenticated():
		return redirect('/login')
	if not request.user.profile.is_administrator():
		return redirect('/')

	student=Student.objects.get(profile_id=user_id)
	passes = Pass.get_passes(student)

	for p in passes:
		p.startReqString = p.startTimeRequested.strftime('%I:%H %p')
		p.endReqString = p.endTimeRequested.strftime('%I:%H %p')
		p.timeLeftString = p.timeLeftOrigin.strftime('%I:%H %p') if p.timeLeftOrigin is not None else '-'
		p.timeArrivedString = p.timeArrivedDestination.strftime('%I:%H %p') if p.timeArrivedDestination is not None else '-'

		p.dateString = p.date.strftime('%a, %B %d')
		p.destinationString = p.get_destination()

	return render(request, "administrator/admin_view.html",
	              {'pass': passes, 'name': student.profile.user.first_name+ ' '+student.profile.user.last_name})

@login_required
def student_home(request):
	if not request.user.is_authenticated():
		return redirect('/login')
	if not request.user.profile.is_student():
		return redirect('/')
	else:
		active = Pass.get_students_active_passes(request.user)
		pending = Pass.get_students_pending_passes(request.user)
		old = Pass.get_students_old_passes(request.user)

		if request.method == "GET":
			request_form = RequestPassForm(user=request.user)

		else:
			request_form = RequestPassForm(request.POST, user=request.user)
			if request_form.is_valid():
				request_form.save()
				return redirect('/student')

		return render(request, "student/student_home.html",
		              {'active': active, 'pending': pending,
		               'old': old,
		               'request_form': request_form})


@login_required
def teacher_home(request):
	if not request.user.is_authenticated():
		return redirect('/login')
	if not request.user.profile.is_teacher():
		return redirect('/')
	incoming = Pass.get_teachers_incoming_student_passes(request.user)
	outgoing = Pass.get_teachers_outgoing_student_passes(request.user)
	unapproved = Pass.get_teachers_unapproved_passes(request.user)
	old = Pass.get_teachers_old_passes(request.user)
	if request.method == "GET":
		create_form = CreatePassForm(user=request.user)

	else:
		create_form = CreatePassForm(request.POST, user=request.user)
		if create_form.is_valid():
			create_form.save()
			return redirect('/teacher')

	return render(request, "teacher/teacher_home.html",
	              {'incoming': incoming, 'outgoing': outgoing,
	               'unapproved': unapproved, 'old': old,
	               'create_form': create_form})


@login_required
def approve(request, pass_id):
	if not request.user.is_authenticated():
		return redirect('/login')
	if not request.user.profile.is_teacher() and not request.user.profile.is_location():
		return redirect('/')
	else:
		try:
			pass_obj = Pass.objects.get(id=pass_id)
		except Pass.DoesNotExist:
			return redirect('/teacher')
		pass_obj.approve(request.user.profile.teacher)
		return redirect('/teacher')


@login_required
def checkin(request, pass_id):
	if not request.user.is_authenticated():
		return redirect('/login')
	if not request.user.profile.is_teacher() and not request.user.profile.is_location():
			return redirect('/')
	else:
		try:
			pass_obj = Pass.objects.get(id=pass_id)
		except Pass.DoesNotExist:
			return redirect('/teacher')
		pass_obj.sign_in(request.user.profile.teacher)
		return redirect('/teacher')


@login_required
def checkout(request, pass_id):
	if not request.user.is_authenticated():
		return redirect('/login')
	if not request.user.profile.is_teacher() and not request.user.profile.is_location():
		return redirect('/')
	else:
		try:
			pass_obj = Pass.objects.get(id=pass_id)
		except Pass.DoesNotExist:
			return redirect('/teacher')
		pass_obj.sign_out(request.user.profile.teacher)
		return redirect('/teacher')

@login_required
def location_home(request):
	if not request.user.is_authenticated():
		return redirect('/login')
	if not request.user.profile.is_location():
		return redirect('/')
	incoming = Pass.get_locations_incoming_student_passes(request.user)
	old = Pass.get_locations_old_passes(request.user)
	if request.method == "GET":
		create_form = CreatePassForm(user=request.user)

	else:
		create_form = CreatePassForm(request.POST, user=request.user)
		if create_form.is_valid():
			create_form.save()
			return redirect('/location')

	return render(request, "location/location_home.html",
	              {'incoming': incoming,
	               'old': old,
	               'create_form': create_form})
