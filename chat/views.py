from django.shortcuts import render, redirect
from .models import Conversation
from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import UserSerializer

def home(request):
    if request.user.is_authenticated:
        conversations = Conversation.get_user_conversations(request.user)
        context = {
            'conversations': conversations
        }

        return render(request, 'chat/home.html', context)
    return redirect('/login')

# screeen for selecting a new conversation
def new(request):
    if request.user.is_authenticated:
        context = {'users': User.objects.all().exclude(id=request.user.id)}
        return render(request, 'chat/select_user.html', context)
    return redirect('/login')


def create_conversation(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        if not Conversation.two_user_conversation_exists(userOne=user, userTwo=request.user):
            Conversation(userOne=request.user, userTwo=user).save()
        return redirect("/chat")
    return redirect("/login")


def conversation(request, conversation_id):
    if request.user.is_authenticated:
        context = {'conversation': Conversation.objects.get(id=conversation_id)}
        return render(request, 'chat/conversation.html', context)
    return redirect('/login')


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = self.queryset.exclude(id=self.request.user.id)
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(username__icontains=username)
        return queryset
