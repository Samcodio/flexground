from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
path('' , views.home, name='home' ),
path('delete_C/<int:pk>/<int:ps>/' , views.delete_comment, name='delete_comment' ),
path('delete_Post/<int:pk>/' , views.delete_post, name='delete_post' ),
path('create/post/' , views.create_post, name='create_post' ),
path('turn_comment/<int:pk>/<str:value>/', views.turn_comment, name='comment_turn' ),
path('comment/<str:author>/<int:pk>/', views.comment, name='comment'),
path('toggle_like/<int:pk>/', views.toggle_like, name='toggle_like'),
path('profile/<int:pk>/', views.profile, name='profile'),

]