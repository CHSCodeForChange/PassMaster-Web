from django.shortcuts import redirect


def home(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    elif request.user.is_superuser:
        return redirect('/admin')
    elif request.user.profile.is_student():
        return redirect('/student')
    elif request.user.profile.is_teacher():
        return redirect('/teacher')
    elif request.user.profile.is_location():
        return redirect('/location')
    else:
        return redirect('/test')
