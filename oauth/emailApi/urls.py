from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('run_schedules/', views.run_schedules),

    path('schedules/', views.schedules),

    path('check/', views.welcome),

]