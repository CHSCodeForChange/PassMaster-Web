from django.shortcuts import render, redirect
from .models import Conversation
from django.contrib.auth.models import User

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        conversations = Conversation.get_conversations(request.user)

        context = {
            'conversations': conversations
        }

        return render(request, 'chat/home.html', context)
    return redirect('/login')


def new(request):
    if request.user.is_authenticated:
        context = {'users': User.objects.all().exclude(id=request.user.id)}
        return render(request, 'chat/select_user.html', context)
    return redirect('/login')


def conversation(request, conversation_id):
    if request.user.is_authenticated:
        return render(request, 'chat/home.html')
    redirect('/login')
