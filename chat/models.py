from django.db import models
from auth_app.models import Accounts


class Message(models.Model):
    sender = models.ForeignKey(Accounts, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Accounts, related_name='received_messages', on_delete=models.CASCADE)
    messages = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} to {self.receiver.username}: {self.messages[:20]}"
