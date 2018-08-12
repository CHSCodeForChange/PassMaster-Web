from django.shortcuts import render, redirect
from .models import Conversation
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        conversations = Conversation.get_user_conversations(request.user)
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


def create_conversation(request, user_id):
    user = User.objects.get(id=user_id)
    Conversation(userOne=request.user, userTwo=user).save()
    return redirect('/chat')


def conversation(request, conversation_id):
    if request.user.is_authenticated:
        context = {'conversation': Conversation.objects.get(id=conversation_id)}
        return render(request, 'chat/conversation.html', context)
    return redirect('/login')
