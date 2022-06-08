from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', home_view, name = 'home'),
    path('room/<str:pk>/', room_view, name = 'room'),
    path('room/<str:pk>/update/', room_update, name = 'update-room'),
    path('room/<str:pk>/delete/', room_delete, name = 'delete-room'),
    path('create-room/', room_create, name = 'create-room'),
    
    path('login/', login_page, name = 'login'),
    path('logout/', logout_page, name = 'logout'),
    path('profile/<str:pk>/', user_profile, name = 'user-profile'),
    path('register/', register_page, name = 'register'),
    
    path('activity/', activity_view , name = 'activity'),
    path('delete_message/<int:pk>/', message_delete, name = 'delete-message'),
    path('topics/', topics_view, name = 'topics'),
    path('update-user/', update_user, name = 'update-user'),
]
