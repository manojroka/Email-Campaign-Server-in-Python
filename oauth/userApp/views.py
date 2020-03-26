
from django.shortcuts import render
from userApp.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from oauth2_provider.models import Application
import requests, base64, json


def index(request):
    if request.user.is_authenticated:
        
        filterUser = Application.objects.filter(user=request.user)
        return render(request,'home.html', {'data':filterUser})
    else:
        return render(request,'home.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('userApp:index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
       
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
      
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
      
    return render(request,'register.html',
                          {'user_form':user_form,

                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('userApp:index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})


@login_required
def appreg(request):
    return HttpResponseRedirect('http://127.0.0.1:8000/o/applications')





@login_required
def gentoken(request):
    filterUser = Application.objects.filter(user=request.user)
    if request.method == 'GET':
        
        return render(request,'token.html', {'data':filterUser})
    elif request.method == 'POST':
        appName = request.POST['appName']
        username = request.POST['username']
        password = request.POST['password']
        print(appName)
        grant=''
        client_id=''
        client_secret=''
        apps = Application.objects.filter(name=appName)
        for a in apps:
            grant = a.authorization_grant_type
            client_id = a.client_id
            client_secret = a.client_secret


        credentials = "%s:%s" % (client_id, client_secret)
        encode_credential = base64.b64encode(credentials.encode('utf-8')).decode('utf-8').replace("\n", "")


        headers = {
            "Authorization": ("Basic %s" % encode_credential),
                  
        }
        data = {
        'grant_type': grant,
        'username': username,
        'password': password
        }
        
        url = 'http://localhost:8000/o/token/'
        r = requests.post(url, headers=headers, data=data)
        # print(r)
        # print(r.text)
        response = json.loads(r.text)
        
        return render(request,'token.html', {'data2':apps,'data':filterUser,'access_data':response} )
    