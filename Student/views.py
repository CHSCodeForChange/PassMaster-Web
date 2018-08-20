from django.shortcuts import render, redirect
from Passes.models import Pass
from django.contrib.auth.decorators import login_required

# Create your views here.
from Student.forms import RequestPassForm
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



def viewPass(request):
    studentPasses = Pass.objects.get(student=request.user)
    return render(request, "student/student_home.html", {'passes': studentPasses})

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

            active = Pass.get_students_active_passes(request.user)
            pending = Pass.get_students_pending_passes(request.user)
            old = Pass.get_students_old_passes(request.user)

            return render(request, "student/student_home.html", {'active': active, 'pending': pending, 'old': old})
        return render(request, 'student/request_pass.html', {'form': form})
