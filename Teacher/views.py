from django.shortcuts import render, redirect
from Passes.models import Pass

# Create your views here.
def home(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_student():
        return redirect('/student')
    else:
        incoming = Pass.get_teachers_incomming_student_passes(request.user)
        outgoing = Pass.get_teachers_outgoing_student_passes(request.user)
        unapproved = Pass.get_teachers_unapproved_passes(request.user)
        old = Pass.get_teachers_old_passes(request.user)

        return render(request, "teacher/home.html",
            {'incoming': incoming, 'outgoing': outgoing,
            'unapproved': unapproved, 'old': old})
