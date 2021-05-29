import os
import json
import requests
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from api_tables.models import User

# Create your views here.

@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html', {})

def login(request):

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['SECRET_KEY'] = os.environ.get("SECRET_KEY")
        json_response = requests.post('http://localhost:8000/api/auth/login/', data=request.POST).json()

        if json_response['authorized'] == 'true':
            user = User.objects.get(id=json_response['user_id'])
            auth_login(request, user)
            return redirect('main-index')
        else:
            return HttpResponse(json_response['error_message']) # TODO CONVERTIR ESTE MENSAJE EN UN NOTIFICATION DEL DASHBOARD

    else:
        return render(request, 'login.html', {})

def logout(request):
    auth_logout(request)
    return redirect('main-login')
