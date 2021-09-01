from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.gallery, name='gallery'),
    path('photo/<str:id>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
]