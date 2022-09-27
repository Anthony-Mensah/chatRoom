from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path('', views.home, name='home'),
    # PROFILE
    path('profile/<str:pk>/', views.profilePage, name='profile'),
    # ROOM
    path('room/<str:pk>/', views.room, name='room'),
    # CREATE ROOM
    path('create-room/', views.createRoom, name='create-room'),
    # UDDATE ROOM
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    # DELETE ROOM
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    # DELETE MESSAGE
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    # ACTIVITIES
    path('activity/', views.activityPage, name='activity'),
    # TOPIC
    path('topic/', views.topicPage, name='topic'),
]
