from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions, serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', "first_name", "last_name"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name",] 



class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')



@api_view(["GET"])

def users(request):
      
    schedules = User.objects.all()
    print(schedules)
    serializer = UserSerializer(schedules, many=True)
    return JsonResponse({'users': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])

def groups(request):
      
    schedules = Group.objects.all()
    print(schedules)
    serializer = GroupSerializer(schedules, many=True)
    return JsonResponse({'groups': serializer.data}, safe=False, status=status.HTTP_200_OK)