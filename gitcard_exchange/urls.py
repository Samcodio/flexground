

from django.urls import path, reverse
from . import views



urlpatterns = [

path('home/', views.excangegiftcard, name='excangegiftcard')

]
