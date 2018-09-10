from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import *


def student_home(request):
	if not request.user.is_authenticated():
		return redirect('/login')
	elif request.user.profile.is_teacher():
		return redirect('/teacher')
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


def teacher_home(request):
	if not request.user.is_authenticated():
		return redirect('/login')
	elif request.user.profile.is_student():
		return redirect('/student')
	incoming = Pass.get_teachers_incoming_student_passes(request.user)
	outgoing = Pass.get_teachers_outgoing_student_passes(request.user)
	unapproved = Pass.get_teachers_unapproved_passes(request.user)
	print(unapproved)
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
	elif request.user.profile.is_student():
		return redirect('/student')
	else:
		try:
			pass_obj = Pass.objects.get(id=pass_id)
		except Pass.DoesNotExist:
			return redirect('/teacher')
		pass_obj.approve(request.profile.teacher)
		return redirect('/teacher')


@login_required
def checkin(request, pass_id):
	if not request.user.is_authenticated():
		return redirect('/login')
	elif request.user.profile.is_student():
		return redirect('/student')
	else:
		try:
			pass_obj = Pass.objects.get(id=pass_id)
		except Pass.DoesNotExist:
			return redirect('/teacher')
		pass_obj.arrive(request.user.profile.teacher)
		return redirect('/teacher')


@login_required
def checkout(request, pass_id):
	if not request.user.is_authenticated():
		return redirect('/login')
	elif request.user.profile.is_student():
		return redirect('/student')
	else:
		try:
			pass_obj = Pass.objects.get(id=pass_id)
		except Pass.DoesNotExist:
			return redirect('/teacher')
		pass_obj.leave(request.user.profile.teacher)
		return redirect('/teacher')
