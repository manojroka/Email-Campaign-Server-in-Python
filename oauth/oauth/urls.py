from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
admin.autodiscover()

from .views import ApiEndpoint, users, groups

from rest_framework import generics, permissions, serializers

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from userApp import urls
from emailApi import urls





# Setup the URLs and include login URLs for the browsable API.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
   
    path('api/users', users),
    path('api/groups', groups),
    path('users/', include('userApp.urls')),
    path('api/email/', include('emailApi.urls')),
    
]
