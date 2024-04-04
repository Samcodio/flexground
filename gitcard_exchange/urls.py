

from django.urls import path
from . import views


app_name = 'gitcard_exchange'


urlpatterns = [

    path('home/', views.excangegiftcard, name='excangegiftcard')

]
