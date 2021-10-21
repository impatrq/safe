import os
import json
import requests
from django.http.response import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from api_tables.models import User
from api_tables.forms import WorkerForm, DoorForm

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html', {'sk': os.environ.get('SECRET_KEY')})

def login(request):

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['SECRET_KEY'] = os.environ.get("SECRET_KEY")
        json_response = requests.post(settings.CURRENT_HOST + '/api/auth/login/', data=request.POST).json()

        if json_response['authorized'] == 'true':
            user = User.objects.get(id=json_response['user_id'])
            auth_login(request, user)
            return redirect('main-index')
        else:
            return render(request, 'login.html', {'error': json_response['error_message']})

    else:
        return render(request, 'login.html', {})

def logout(request):
    auth_logout(request)
    return redirect('main-login')

@login_required(login_url='/login/')
def workers(request):
    form = WorkerForm()
    return render(request, 'workers.html', {'form': form, 'sk': os.environ.get('SECRET_KEY')})

@login_required(login_url='/login/')
def doors(request):
    form = DoorForm()
    return render(request, 'doors.html', {'form': form, 'sk': os.environ.get('SECRET_KEY')})

@login_required(login_url='/login/')
def logs(request):
    return render(request, 'logs.html', {'sk': os.environ.get('SECRET_KEY')})

def about_us(request):
    return render(request, 'about-us.html', {})