from django.db.models import Q
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Message

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


#@login_required
def list_superusers_view(request):
    if request.user.is_superuser:
        # Redirect superusers somewhere else, as they shouldn't be sending messages to other superusers
        return redirect('home')

    superusers = User.objects.filter(is_superuser=True)
    return render(request, 'choose.html', {'superusers': superusers})




@login_required


def send_message(request, superuser_id):

    superuser = get_object_or_404(User, pk=superuser_id, is_superuser=True)



    # Retrieve messages between the user and the superuser
    messages = Message.objects.filter(Q(sender=request.user, recipient=superuser)
                                      | Q(sender=superuser, recipient=request.user)).order_by('date')


    if request.method == 'POST':
        body = request.POST.get('body')
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
        return render(request, 'superuser.html', {'superuser': superuser, 'messages': messages})

def excangegiftcard(request):

    context = {}
    return render(request,'gitcard_exchange/index.html')
