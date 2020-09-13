from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('lastPosts', views.lastPosts, name='lastPosts'),
    path('checkWord/', views.checkWord, name='checkWord')
]