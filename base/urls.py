from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.LoginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout!/", views.logoutUser, name="logout"),
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:pk>/", views.UpdateRoom, name="update-room"),
    path("profile/<str:pk>/", views.userProfile, name="user-profile"),
    path("update-user/", views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),
    path("delete-message/<str:pk>/", views.deleteMessage, name="delete-message"),
]
