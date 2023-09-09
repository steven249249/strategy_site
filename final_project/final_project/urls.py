"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hamlet.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',board_all),
    path('login/',login,name='login-url'),
    path('logout/',logout,name='logout-url'),
    path('board_all/',board_all),
    path('board_all/<int:page>/',board_all,name='board_all-url'),
    path('post/<int:postid>/',post, name='post-url'),
    path('share/<int:postid>/',share),
    path('remove/<int:postid>/',remove),
    path('alter_post/<int:postid>/',alter_post),
    path('alter_comment/<int:commentid>/',alter_comment),
    path('remove_comment/<int:commentid>/',remove_comment),
    path('board/<str:board_name>/',board),
    path('board/<str:board_name>/<int:page>/', board, name='board-url'),
    path('add_post/<str:board_name>/', add_post, name='add_post-url'),
    path('send_msg', send_msg, name='send_msg'),
    path('get_msg/<str:board_name>/', get_msg, name='get_msg'),
    path('home/',home),
    path('home/<int:userid>/',home,name='home-url'),
    path('alter/<int:userid>/',alter,name='alter-url'),
    path('collected/<int:userid>/',collected,name='collected-url'),
    path('sharelist/<int:userid>/',sharelist,name='sharelist-url'),
    path('inform/<int:userid>/',inform,name='inform-url'),
    path('register/',register),
    path('ban/<int:userid>/',ban,name='ban-url'),
]
