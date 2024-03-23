from django.shortcuts import render, redirect, reverse

# Create your views here.


def dashboard(request):
    context = {}
    return render(request, 'take_app/index.html', context)
