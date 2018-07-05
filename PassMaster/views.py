from django.shortcuts import redirect
from Student import views as student
from Teacher import views as teacher

def home(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.is_superuser:
        return redirect('/admin')
    elif request.user.profile.is_student():
        return redirect('/student')
    elif request.user.profile.is_teacher():
        return redirect('/teacher')
    else:
        return redirect('/test')
