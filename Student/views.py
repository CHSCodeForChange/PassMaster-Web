from django.shortcuts import render, redirect
from Passes.models import Pass

# Create your views here.
def home(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_teacher():
        return redirect('/teacher')
    else:
        active = Pass.get_students_active_passes(request.user)
        pending = Pass.get_students_pending_passes(request.user)
        old = Pass.get_students_old_passes(request.user)

        return render(request, "student/home.html", {'active': active, 'pending': pending, 'old': old})
