from django.conf.urls import url
from django.urls import path, include
from userApp import views

app_name = 'userApp'
urlpatterns = [
   
    path('register', views.register, name='register'),
    path('', views.index, name='index'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='logout'),
    path('reg_app', views.appreg, name='reg_app'),
 
    path('gen_token', views.gentoken, name='gen_token')
    
]