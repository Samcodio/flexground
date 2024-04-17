from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
     path('home/', views.excangegiftcard, name='excangegiftcard'),
     path('list_buyers/', views.list_superusers_view, name='list_superusers_view'),
     path('message/0067889077555/0985567880099876543234555667/46556677889/<int:superuser_id>/', views.send_message, name='send_message'),
     path('messages/M0067889077555H/0985K56788009987OO654323I4555667/4655F66778J89/<int:superuser_id>/', views.send_message_n, name='send_message_n'),
     path('message/', views.message, name='message'),
     path('inbox/', views.inbox, name='inbox'),
    


]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

