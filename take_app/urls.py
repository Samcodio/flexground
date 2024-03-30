from django.urls import path
from . import views  # This imports the views from your views.py file

app_name = 'take_app'  # This is fine to define here if you're using app-specific namespacing

urlpatterns = [
    path('', views.home, name='home'),  # Connects the root URL of the app to the home view
]
