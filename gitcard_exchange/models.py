from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient}'

    @classmethod
    def send_message(cls, sender, recipient, body, image=None, video=None):
        if sender.is_superuser:
            raise ValueError("Superusers cannot send messages.")
        message = cls(sender=sender, recipient=recipient, body=body, image=image, video=video)
        message.save()
        return message

    @classmethod
    def get_messages(cls, user):
        if user.is_superuser:
            messages = cls.objects.filter(recipient=user).values('sender').annotate(last_date=Max('date')).order_by('-last_date')
        else:
            messages = cls.objects.filter(recipient=user, sender__is_superuser=True).values('sender').annotate(last_date=Max('date')).order_by('-last_date')

        users = []
        for message in messages:
            sender = User.objects.get(pk=message['sender'])
            unread_count = cls.objects.filter(recipient=user, sender=sender, is_read=False).count()
            users.append({
                'sender': sender,
                'last_date': message['last_date'],
                'unread': unread_count,
            })

        return users


class Inbox(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='inbox')
    messages = models.ManyToManyField(Message)

    def get_unread_messages(self):
        return self.messages.filter(is_read=False)

    def get_latest_message(self):
        return self.messages.latest('date')

    def mark_all_as_read(self):
        unread_messages = self.get_unread_messages()
        unread_messages.update(is_read=True)