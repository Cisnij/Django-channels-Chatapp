from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="home"),
    path('friends/<str:pk>',views.detail,name="detail"),
    path('sendMessage/<str:pk>',views.sendMessage,name="sendMessage"),
    path('receiveMessage/<str:pk>',views.receiveMessage,name="receiveMessage"),
    path('login/',views.Login,name="login"),
    path('register/',views.Register,name="register"),
    path('logout/',views.Logout,name="logout"),
    path('addfriend/',views.addFriend,name="addfriend"),
    path('acceptFriend/',views.acceptFriend,name="acceptFriend"),
    path('notification/',views.Notification,name="notification"),
    path('profile/',views.ProfileUser,name="profile"),
]