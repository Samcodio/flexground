from django.shortcuts import render

# Create your views here.
def excangegiftcard(request):

    context = {}
    return render(request,'gitcard_exchange/index.html')