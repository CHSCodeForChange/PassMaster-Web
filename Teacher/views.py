from django.shortcuts import render, redirect
from Passes.models import Pass

# Create your views here.
def home(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_student():
        return redirect('/student')
    else:
        incoming = Pass.get_teachers_incoming_student_passes(request.user)
        outgoing = Pass.get_teachers_outgoing_student_passes(request.user)
        unapproved = Pass.get_teachers_unapproved_passes(request.user)
        old = Pass.get_teachers_old_passes(request.user)

        return render(request, "teacher/home.html",
            {'incoming': incoming, 'outgoing': outgoing,
            'unapproved': unapproved, 'old': old})

def approve(request, pass_id):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_student():
        return redirect('/student')
    else:
        thepass = Pass.objects.get(id=pass_id)
        thepass.approve()
        incoming = Pass.get_teachers_incoming_student_passes(request.user)
        outgoing = Pass.get_teachers_outgoing_student_passes(request.user)
        unapproved = Pass.get_teachers_unapproved_passes(request.user)
        old = Pass.get_teachers_old_passes(request.user)

        return render(request, "teacher/home.html",
            {'incoming': incoming, 'outgoing': outgoing,
            'unapproved': unapproved, 'old': old})

def checkin(request, pass_id):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_student():
        return redirect('/student')
    else:
        thepass = Pass.objects.get(id=pass_id)
        thepass.arrive()
        print(thepass.timeArrived)
        incoming = Pass.get_teachers_incoming_student_passes(request.user)
        outgoing = Pass.get_teachers_outgoing_student_passes(request.user)
        unapproved = Pass.get_teachers_unapproved_passes(request.user)
        old = Pass.get_teachers_old_passes(request.user)

        return render(request, "teacher/home.html",
            {'incoming': incoming, 'outgoing': outgoing,
            'unapproved': unapproved, 'old': old})

def checkout(request, pass_id):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_student():
        return redirect('/student')
    else:
        thepass = Pass.objects.get(id=pass_id)
        thepass.leave()
        print(thepass.timeLeft)
        incoming = Pass.get_teachers_incoming_student_passes(request.user)
        outgoing = Pass.get_teachers_outgoing_student_passes(request.user)
        unapproved = Pass.get_teachers_unapproved_passes(request.user)
        old = Pass.get_teachers_old_passes(request.user)

        return render(request, "teacher/home.html",
            {'incoming': incoming, 'outgoing': outgoing,
            'unapproved': unapproved, 'old': old})


    #return redirect('teacher/home.html"' + str(slot.id))
