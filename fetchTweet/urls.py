from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('userTweets', views.userTweets, name='userTweets'),
    path('keyWordTweets', views.keyWordTweets, name='keyWordTweets'),
    # path('another', views.index, name='index'),
    # path('<str:room_name>/', views.room, name='room'),
]