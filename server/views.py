from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import *


def requestPass(request):
	pass


def editPass(request):
	pass


def approvePass(request, pass_id):
	# check if the logged in user is a teacher, is assigned ot the pass, and that the pass is not approved yet
	if request.user.profile.is_teacher():
		# get pass that was given
		currPass = Pass.objects.get(id=pass_id)

		if request.user.profile.Teacher == currPass.originTeacher:
			if not currPass.approved:
				currPass.approve()  # set the pass to approved
				print("Approved")
			else:
				print("This user is already approved")
		else:
			print("You are not assigned to this pass")
	else:
		print("You are not a teacher")


def leave(request, pass_id):
	# check if the logged in user is a teacher
	if request.user.profile.is_teacher():
		# get pass that was given
		currPass = Pass.objects.get(id=pass_id)

		# check if the teacher is assgineed to the pass
		if request.user.profile.Teacher == currPass.originTeacher:

			# check if the pass is approved
			if currPass.approved:
				currPass.leave()  # set the pass to approved
				print("Left")
			else:
				print("This user is already approved")
		else:
			print("You are not assigned to this pass")
	else:
		print("You are not a teacher")


def arrive(request, pass_id):
	# check if the logged in user is a teacher
	if request.user.profile.is_teacher():
		# get pass that was given
		currPass = Pass.objects.get(id=pass_id)

		# check if the teacher is assgineed to the pass
		if request.user.profile.Teacher == currPass.originTeacher:

			# check if the pass is approved
			if currPass.approved:
				currPass.arrive()  # set the pass to approved
				print("Arrived")
			else:
				print("This user is already approved")
		else:
			print("You are not assigned to this pass")
	else:
		print("You are not a teacher")


# Student


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


@login_required
def requestPass(request):
	if not request.user.is_authenticated():
		return redirect('/login')

	if request.method == 'GET':
		form = RequestPassForm(user=request.user)
		return render(request, 'student/request_pass.html', {'form': form})
	else:
		form = RequestPassForm(request.POST, user=request.user)
		if form.is_valid():
			data = form.save(commit=False)
			data.save()

			return redirect('/student')
		return render(request, 'student/request_pass.html', {'form': form})

# Teacher
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
		if pass_obj.originTeacher == request.user.profile.teacher:
			pass_obj.approve()
		return redirect('/teacher')


@login_required
def checkin(request, pass_id):
	if not request.user.is_authenticated():
		return redirect('/login')
	elif request.user.profile.is_student():
		return redirect('/student')
	else:
		try:
			pass_obj = TeacherPass.objects.get(id=pass_id)
		except TeacherPass.DoesNotExist:
			return redirect('/teacher')
		if pass_obj.destinationTeacher == request.user.profile.teacher:
			pass_obj.arrive()
		return redirect('/teacher')


@login_required
def checkout(request, pass_id):
	if not request.user.is_authenticated():
		return redirect('/login')
	elif request.user.profile.is_student():
		return redirect('/student')
	else:
		try:
			pass_obj = TeacherPass.objects.get(id=pass_id)
		except TeacherPass.DoesNotExist:
			return redirect('/teacher')
		if pass_obj.originTeacher == request.user.profile.teacher:
			pass_obj.leave()
		return redirect('/teacher')
