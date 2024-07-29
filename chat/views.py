# messages/views.py

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Max
from .models import Message, Accounts
from .serializers import UserListSerializer

class MessagedUsers(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        senders = Message.objects.filter(receiver=user).values_list('sender', flat=True).distinct()
        senders_accounts = Accounts.objects.filter(id__in=senders)

        serializer = UserListSerializer(senders_accounts, many=True, context={'request': request})
        return Response(serializer.data)
