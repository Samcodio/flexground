# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment

@receiver(post_save, sender=Comment)
def create_mention_notifications(sender, instance, created, **kwargs):
    if created:
        instance.parse_mentions()
