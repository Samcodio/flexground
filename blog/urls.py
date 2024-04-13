from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
path('' , views.home, name='home' ),
path('create/post/' , views.create_post, name='create_post' ),
path('comment/<str:author>/<int:pk>/', views.comment, name='comment'),
path('toggle_like/<int:pk>/', views.toggle_like, name='toggle_like'),

]