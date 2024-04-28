from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
import re
from django.dispatch import receiver
from django.db.models.signals import post_save



class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    comment_turn = models.CharField(max_length=10, default='on')

    def __str__(self):
        return self.title

class BlogMedia(models.Model):
    blog = models.ForeignKey(Blog, related_name='media', on_delete=models.CASCADE)
    media_file = models.FileField(upload_to='blog_media/', blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def share_count(self):
        return self.shares.count()

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username} on {self.blog.title}"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.parse_mentions()

    def parse_mentions(self):
        mentions = re.findall(r'@(\w+)', self.text)
        for username in set(mentions):
            try:
                user = User.objects.get(username=username)
                Notification.create_notification(user, 'mention', self)
            except User.DoesNotExist:
                continue

class Share(models.Model):
    blog = models.ForeignKey(Blog, related_name='shares', on_delete=models.CASCADE)
    sharer = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    account_strength = models.CharField(
        max_length=6,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium'
    )
    enable_notifications = models.BooleanField(default=True)
    theme_preference = models.CharField(max_length=10, default='light')  # Example: light or dark theme

    def __str__(self):
        return f"Settings for {self.user.username}"

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=[('system', 'System'), ('user', 'User'), ('message', 'Message')], default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.recipient.username} - {self.title}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()

@receiver(post_save, sender=Share)
def create_share_notification(sender, instance, created, **kwargs):
    if created:
        recipient = instance.blog.author  # Assuming the author of the shared blog is the recipient
        Notification.objects.create(
            recipient=recipient,
            title="New Share",
            message=f"Your Post '{instance.blog.title}' has been shared by {instance.sharer.username}."
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created:
        recipient = instance.blog.author  # Assuming the author of the commented blog is the recipient
        Notification.objects.create(
            recipient=recipient,
            title="New Comment",

            message=f"Your Post '{instance.blog.title}' has received a new comment from {instance.commenter.username}."
        )