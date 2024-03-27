from django.urls import path
from . import views


app_name = 'user_login'


urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('reg_user/', views.register_user, name='register')
]
