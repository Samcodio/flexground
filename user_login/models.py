from django.db import models

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields like profile picture, bio, etc.


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    # Add fields for voice notes, images, etc.
    created_at = models.DateTimeField(auto_now_add=True)
