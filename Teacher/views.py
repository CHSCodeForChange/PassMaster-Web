from django.shortcuts import render, redirect
from Passes.models import Pass

# Create your views here.
from Teacher.forms import CreatePassForm


def home(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_student():
        return redirect('/student')
    incoming = Pass.get_teachers_incoming_student_passes(request.user)
    outgoing = Pass.get_teachers_outgoing_student_passes(request.user)
    print(outgoing)
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

def approve(request, pass_id):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_student():
        return redirect('/student')
    else:
        thepass = Pass.objects.get(id=pass_id)
        thepass.approve()


        return redirect('/teacher')

def checkin(request, pass_id):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_student():
        return redirect('/student')
    else:
        thepass = Pass.objects.get(id=pass_id)
        thepass.arrive()

        return redirect('/teacher')


def checkout(request, pass_id):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.profile.is_student():
        return redirect('/student')
    else:
        thepass = Pass.objects.get(id=pass_id)
        thepass.leave()

        return redirect('/teacher')



    #return redirect('teacher/teacher_home.html"' + str(slot.id))
