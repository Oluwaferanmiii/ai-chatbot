from django.db import models
from django.contrib.auth.models import User


class ChatSession(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} ({self.created_at})"


class Message(models.Model):
    session = models.ForeignKey(
        ChatSession, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.CharField(max_length=10, choices=[
                              ('user', 'User'), ('bot', 'Bot')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender} @ {self.timestamp}: {self.content[:30]}"
