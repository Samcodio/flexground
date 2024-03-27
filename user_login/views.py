from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm

# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('take_app:home')
        else:
            messages.error(request, 'Invalid details')
    context = {
    }
    return render(request, 'authenticate/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('user_login:login')


def register_user(request):
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User successfully registered')
            return redirect('user_login:login')
        else:
            form = CreateUserForm()
            messages.info(request, 'Details invalid')
    context = {
        'form': form
    }
    return render(request, 'authenticate/register.html', context)
