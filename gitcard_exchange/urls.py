from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
     path('home/', views.excangegiftcard, name='excangegiftcard'),
     path('list_buyers/', views.list_superusers_view, name='list_superusers_view'),
     path('message/<int:superuser_id>/', views.send_message, name='send_message'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

