from django.shortcuts import render, redirect

from Passes.models import Pass


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
                currPass.approve() #set the pass to approved
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
            if  currPass.approved:
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
            if  currPass.approved:
                currPass.arrive()  # set the pass to approved
                print("Arrived")
            else:
                print("This user is already approved")
        else:
            print("You are not assigned to this pass")
    else:
        print("You are not a teacher")

