from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Message
from django.db.models import Q
class ReplyMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body', 'image', 'video']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = 'Reply Message'

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'body', 'date', 'is_read', 'reply_link')
    search_fields = ('sender__username', 'recipient__username', 'body')
    list_filter = ('date', 'sender', 'recipient', 'is_read')

    def reply_link(self, obj):
        url = reverse("admin:exchange_message_reply", args=[obj.pk, obj.recipient.pk])
        print("Generated URL:", url)
        return mark_safe(f'<a href="{url}">Reply</a>')

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:message_id>/<int:normal_user_id>/reply/', self.reply_view, name='exchange_message_reply'),
        ]
        return custom_urls + urls

    def reply_view(self, request, message_id, normal_user_id):
        # Get the message object corresponding to the provided message_id
        # Retrieve the normal user object based on the provided ID
        print(message_id,normal_user_id)
        normal_user = get_object_or_404(User, pk=normal_user_id)
        message = Message.objects.get(pk=message_id)

        # Determine the admin user
        admin_user = request.user

        # Retrieve the messages between the admin user and the sender/recipient of the selected message
        messages = Message.objects.filter(
            Q(sender=admin_user, recipient=normal_user) | Q(sender=normal_user, recipient=admin_user)
        ).order_by('date')

        initial_data = {
            'sender': message.recipient,
            'recipient': message.sender,
        }

        form = ReplyMessageForm(request.POST or None, initial=initial_data)
        if request.method == 'POST' and form.is_valid():
            form.instance.sender = message.recipient
            form.instance.recipient = message.sender
            form.save()
            return redirect(reverse('admin:exchange_message_reply', args=[message_id, normal_user_id]))

        context = {'form': form, 'message': message, 'messages': messages, 'admin_user': admin_user}
        return render(request, 'admin/exchange/message/reply_form.html', context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(sender=request.user)  # Limit queryset to messages sent by the current user (admin)
admin.site.register(Message, MessageAdmin)