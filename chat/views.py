from datetime import datetime

from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions

from .serializers import *
from .models import Conversation

def home(request):
    if request.user.is_authenticated:
        conversations = Conversation.get_user_conversations(request.user)
        context = {
            'conversations': conversations
        }

        return render(request, 'chat/chat_home.html', context)
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


class UserView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset.exclude(id=self.request.user.id)
        username = self.request.query_params.get('username', None)
        count = self.request.query_params.get('count', None)
        if username is not None:
            queryset = queryset.filter(username__icontains=username)
        if count is not None: 
            queryset = queryset[:int(count)]
        return queryset

class MessageView(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation = self.request.query_params.get('conversation', None)
        if conversation is not None:
            conversation = Conversation.objects.get(id=conversation)
            queryset = conversation.messages
        else:
            queryset = Conversation.get_messages(self.request.user)
        return queryset

    def perform_create(self, serializer):
        conversation = Conversation.objects.get(id=int(self.request.data['conversation']))
        if conversation.is_member(self.request.user):
            serializer.save(sender=self.request.user, datetime=datetime.now())
