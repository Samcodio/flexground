from django.db.models import Q
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Message
from gitcard_exchange.arrays import detect as detects
 
 
from django.db.models import Max
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def list_superusers_view(request):
    if request.user.is_superuser:
        # Redirect superusers somewhere else, as they shouldn't be sending messages to other superusers
        return redirect('home')

    superusers = User.objects.filter(is_superuser=True)
    return render(request, 'choose.html', {'superusers': superusers})

def message(request):
    if request.user.is_superuser:
        # Redirect superusers somewhere else, as they shouldn't be sending messages to other superusers
        return redirect('home')
    superusers = User.objects.filter(is_superuser=False)
    return render(request, 'general.html', {'superusers': superusers})
    

 
@login_required
def send_message(request, superuser_id):
    superuser = get_object_or_404(User, pk=superuser_id, is_superuser=True)
    
    messages = Message.objects.filter(Q(sender=request.user, recipient=superuser) |
                                      Q(sender=superuser, recipient=request.user)).order_by('date')

    if request.method == 'POST':
        body = request.POST.get('body')
        
        if_word_is_okay = detects(body.split(' '))
        print(if_word_is_okay)
        
        if if_word_is_okay != False:
            image = request.FILES.get('image') if 'image' in request.FILES else None
            video = request.FILES.get('video') if 'video' in request.FILES else None

            # Example validation: ensure the file size is under 5MB
            if image and image.size > 5 * 1024 * 1024:
                return HttpResponse("Image file too large ( > 5MB ).", status=400)
            if video and video.size > 20 * 1024 * 1024:
                return HttpResponse("Video file too large ( > 20MB ).", status=400)

            # Assuming send_message is correctly implemented to handle the message sending
            Message.send_message(sender=request.user, recipient=superuser, body=body, image=image, video=video)

            # Redirect back to the same page after sending the message
            return redirect('send_message', superuser_id=superuser_id)
        else:
            return HttpResponse("Such words are not allowed. You may be banned soon if you continue...", status=400)
    else:
        return render(request, 'superuser.html', {'superuser': superuser, 'messages': messages})


@login_required
def send_message_n(request, superuser_id):
    try:
        normal_user = get_object_or_404(User, id=superuser_id, is_superuser=False)
        
        messages = Message.objects.filter(Q(sender=request.user, recipient=normal_user) |
                                          Q(sender=normal_user, recipient=request.user)).order_by('date')
        
        if request.method == 'POST':
            body = request.POST.get('body')
            
            if_word_is_okay = detects(body.split(' '))
            print(if_word_is_okay)
            
            if if_word_is_okay != False:
                image = request.FILES.get('image') if 'image' in request.FILES else None
                video = request.FILES.get('video') if 'video' in request.FILES else None

                # Example validation: ensure the file size is under 5MB
                if image and image.size > 5 * 1024 * 1024:
                    return HttpResponse("Image file too large ( > 5MB ).", status=400)
                if video and video.size > 20 * 1024 * 1024:
                    return HttpResponse("Video file too large ( > 20MB ).", status=400)

                # Assuming send_message is correctly implemented to handle the message sending
                Message.send_message(sender=request.user, recipient=normal_user, body=body, image=image, video=video)

                # Redirect back to the same page after sending the message
                return redirect('send_message_n', superuser_id=superuser_id)
            else:
                return HttpResponse("Such words are not allowed. You may be banned soon if you continue...", status=400)
        else:
            return render(request, 'normaluser.html', {'superuser': normal_user, 'messages': messages})
    except User.DoesNotExist:
        return HttpResponse("User not found.", status=404)

def excangegiftcard(request):

    context = {}
    return render(request,'gitcard_exchange/index.html')





 
@login_required
def inbox(request):
    # Get the latest message for each unique sender or recipient
    inbox_messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).values('sender', 'recipient').annotate(latest_date=Max('date'))

    # Query to get the complete message objects corresponding to the latest messages
    latest_messages = Message.objects.filter(date__in=[msg['latest_date'] for msg in inbox_messages])
    unread_messages = Message.objects.filter(recipient=request.user, is_read=False)

    # Mark unread messages as read when rendering the inbox
    for message in unread_messages:
        message.is_read = True
        message.save()
    # Create a dictionary to store the latest message for each unique user
    users_latest_messages = {}
    for message in latest_messages:
        other_user = message.sender if message.recipient == request.user else message.recipient
        if other_user not in users_latest_messages:
            users_latest_messages[other_user] = message

    return render(request, 'gitcard_exchange/inbox.html', {'users_latest_messages': users_latest_messages,'unread_messages':unread_messages})

 