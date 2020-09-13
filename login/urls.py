from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.log, name='log'),
    path('utente/<int:pk>/', views.detUser)
]