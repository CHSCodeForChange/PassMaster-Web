from django.shortcuts import render, redirect
from Passes.models import Pass
from django.contrib.auth.decorators import login_required

# Create your views here.
from Student.forms import RequestForm
from Student.models import Student


def home(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_teacher():
        return redirect('/teacher')
    else:
        active = Pass.get_students_active_passes(request.user)
        pending = Pass.get_students_pending_passes(request.user)
        old = Pass.get_students_old_passes(request.user)

        return render(request, "student/student_home.html", {'active': active, 'pending': pending, 'old': old})


def viewPass(request):
    studentPasses = Pass.objects.get(student=request.user)
    return render(request, "student/student_home.html", {'passes': studentPasses})

@login_required
def requestPass(request):
    if not request.user.is_authenticated():
        return redirect('/login')

    if request.method == 'GET':
        form = RequestForm(user=request.user)
        return render(request, 'student/request_pass.html', {'form': form})
    else:
        form = RequestForm(request.POST, user=request.user)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            active = Pass.get_students_active_passes(request.user)
            pending = Pass.get_students_pending_passes(request.user)
            old = Pass.get_students_old_passes(request.user)

            return render(request, "student/student_home.html", {'active': active, 'pending': pending, 'old': old})
        return render(request, 'student/request_pass.html', {'form': form})
