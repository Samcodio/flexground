from django.shortcuts import render,redirect,  get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import   login_required
from django.contrib import messages
from django.contrib.auth.forms  import UserCreationForm
from .models import Room , Topic, Message
from .forms import RoomForm, UserForm
from django.db.models import Q

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    rooms = Room.objects.filter(
        Q(topic__name__icontains= q) |
        Q(name__icontains= q)|
        Q(description__icontains= q)
                                
                                
                                )
    room_count = rooms.count()
    topics = Topic.objects.all()[0:5]
    context = {"rooms": rooms , 'topics': topics,
                'room_count': room_count,
                'room_messages': room_messages

                }
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all() 
    participants = room.participants.all()
    if request.method == 'POST':
        message  = Message.objects.create(
            body = request.POST.get('body'),
            user = request.user,
            room=room
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {"room": room, 'room_messages': room_messages, 'participants': participants}
    return render(request, "base/room.html", context)
 
def LoginPage(request):
    page = 'login'
    context = {'page': page}
    if request.user.is_authenticated:
        messages.error(request, "Apologies You're Already Logged in!  ")
        return redirect('home')
    if request.method == "POST":

        username = request.POST.get("username").lower()
        password =request.POST.get("password")
        try:
            user = User.objects.get(username=username)
            
        except:
            messages.error(request, "system Error!   ")
        user = authenticate(request, username=username,password=password)
        if user is not None:

            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password doesn't exist! check and try again")

    return render(request, 'base/login_register.html' , context)





def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'sorry!, something went wrong! we are trying to fix it!')
    context = {'page': page , 'form': form}
    return render(request, 'base/login_register.html', context)




@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    create = "create"
    context = {'form': form, 'create': create, 'topics': topics}
    
    if request.method == 'POST':
       topic_name = request.POST.get('topic')
       topic , created = Topic.objects.get_or_create(name=topic_name)
       Room.objects.create(
           host=request.user,
           topic=topic,
           name=request.POST.get('name'),
           description =request.POST.get('description')

       )
       return redirect('home')
       """  form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home') """

    return render (request,'base/room_form.html', context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user , 
               'rooms': rooms,
               'room_messages': room_messages,
               'topics': topics,
               }
    
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def UpdateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        messages.error(request, "Sorry! you're not  the foundation! and can't   update! this room")
        return redirect(  'home')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST, instance=room)# instance is just like id the room passed in is for id detecting the room tp update
        room.name = request.POST.get('name')
        room.topic =  topic
        room.description = request.POST.get('description')
        room.save()
         
        return redirect('home')
    context = {'form': form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html',context  )


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        messages.error(request, "Sorry! you're not  the foundation! and can't   delete! this room")
        return redirect(  'home')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html',{'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
     
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        messages.error(request, "Apologies! you cannot delete this message.")
        return redirect(  'room' , pk=room.id)
    if request.method == 'POST':
        message.delete()
        messages.error(request, " you've deleted the message.")
      
        return redirect('room', pk=message.room.id)
    return render(request, 'base/delete.html',{'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid:
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update-user.html',{'form':form})



def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})