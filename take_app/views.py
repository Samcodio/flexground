from django.shortcuts import render, redirect, reverse

# Create your views here.


def home(request):
    context = {}
    return render(request, 'take_app/index.html', context)



