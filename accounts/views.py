from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm
from django.contrib import messages

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
    return redirect('accounts:login')


def register(request):
    form = RegistrationForm
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('take_app:home')
        else:
            form = RegistrationForm()
            messages.error(request, 'Please Check your username and password')
    context = {
        'form': form
    }
    return render(request, "authenticate/registration.html", context)

