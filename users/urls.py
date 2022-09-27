from django.urls import path
from . import views

urlpatterns = [
    # REGISTER
    path('register', views.register, name='register'),
    # LOGIN
    path('login', views.loginPage, name='login'),
    # LOGOUT
    path('logout', views.logoutPage, name='logout'),
    # uSER USER
    path('update-user/', views.updateUser, name='update-user'),
]
