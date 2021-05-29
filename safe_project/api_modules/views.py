import os
import json
from django.http.response import HttpResponseServerError
import requests
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from requests.api import head
from api_tables.models import Worker, Door

# Create your views here.

def save_log(request, serialized_worker, worker, door, facemask, temperature, authorized):

    data = {
            'SECRET_KEY': os.environ.get('SECRET_KEY'),
            'user_id': worker.user_id.id,
            'worker_id': worker.id,
            'door_id': door.id,
            'facemask': facemask,
            'temperature': temperature,
            'authorized': authorized,
        }

    file = request.FILES['worker_image'].file.getvalue()
    files = {'worker_image': (f'{worker.first_name}{worker.last_name}-{datetime.now().strftime("%Y-%m-%dat%H-%M-%S")}.png', file)}

    response = requests.post('http://localhost:8000/api/tables/logs/create/', data=data, files=files)

    if response.status_code == 200:
        json_response = response.json()
        if json_response['error_message']:
            return JsonResponse(json_response)
        else:
            if facemask == 'true':
                if temperature < 37:
                    return JsonResponse({
                        'error_message': None,
                        'success_message': 'Allowed',
                        'worker': serialized_worker,
                        'worker_image': settings.CURRENT_HOST + worker.worker_image.url,
                    })
                else:
                    return JsonResponse({
                        'error_message': 'Not allowed, temperature higher than it should.',
                        'success_message': None,
                    })
            else:
                return JsonResponse({
                    'error_message': 'Not allowed, no facemask detected.',
                    'success_message': None,
                })  
    elif response.status_code == 403:
        return HttpResponseForbidden()
    else:
        return HttpResponseServerError()

def init(request):
    pass

@csrf_exempt
def verify(request):
    
    if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):
        
        code = request.POST['code']
        temperature = float(request.POST['temperature'])
        facemask = request.POST['facemask']
        mac = request.POST['mac']

        try:
            worker = Worker.objects.get(card_code=code)
            door = Door.objects.get(mac=mac)

            serialized_worker = serializers.serialize('json', [worker, ])

            if facemask == 'true' and temperature < 37:
                return save_log(request, serialized_worker, worker, door, facemask, temperature, 'true')
            else:
                return save_log(request, serialized_worker, worker, door, facemask, temperature, 'false')

        except ObjectDoesNotExist:
            return JsonResponse({
                'error_message': 'Not allowed',
                'success_message': None,
            })
        except Exception as e:
            return JsonResponse({
                'error_message': f'Error: {e}',
                'success_message': None,
            })
    else:
        return HttpResponseForbidden()


def env_update(request):
    pass