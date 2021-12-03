from django.contrib import admin
from django.urls import path
from . import views

app_name = 'users_app'

urlpatterns = [
    path(
        'register/', 
        views.UserCreateView.as_view(),
        name='user-register'
    ),
    path(
        'login/', 
        views.Login.as_view(),
        name='login'
    ),
    path(
        'logout/', 
        views.Logout.as_view(),
        name='logout'
    ),
    path(
        'updatep/', 
        views.ActualizarContrasena.as_view(),
        name='updatep'
    ),
    path(
        'validacion/<pk>/', 
        views.ValidarUser.as_view(),
        name='validacion'
    ),
]
