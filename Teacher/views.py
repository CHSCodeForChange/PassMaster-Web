from django.shortcuts import render, redirect
from Passes.models import Pass, TeacherPass

# Create your views here.
from Teacher.forms import CreatePassForm


def home(request):
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

