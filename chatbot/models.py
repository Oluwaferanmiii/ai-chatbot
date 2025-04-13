from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.CharField(max_length=10, choices=[
                              ('user', 'User'), ('bot', "Bot")])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"{self.sender} at {self.timestamp}: {self.content[:30]}"
