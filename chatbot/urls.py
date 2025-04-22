from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new-chat/', views.new_chat, name='new_chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('', views.login_user, name='root'),
]
