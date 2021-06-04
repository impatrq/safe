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
from api_tables.models import Worker, Door, Logs

# Create your views here.

def save_log(request, worker, door, facemask, temperature, sanitizer_perc, authorized):

    serialized_worker = serializers.serialize('json', [worker, ])

    data = {
            'SECRET_KEY': os.environ.get('SECRET_KEY'),
            'user_id': worker.user_id.id,
            'worker_id': worker.id,
            'door_id': door.id,
            'facemask': facemask,
            'temperature': temperature,
            'authorized': authorized,
        }

    file = request.FILES['worker_image'].file.getvalue()                                                                                # Obtenemos los datos de la imagen codificados
    files = {'worker_image': (f'{worker.first_name}{worker.last_name}-{datetime.now().strftime("%Y-%m-%dat%H-%M-%S")}.png', file)}      # Creamos el diccionario que le pasamos al request con el nombre de la foto formateado

    response = requests.post(settings.CURRENT_HOST + '/api/tables/logs/create/', data=data, files=files)

    if response.status_code == 200:
        json_response = response.json()
        if json_response['error_message']:
            return JsonResponse(json_response)
        else:
            if facemask == 'true':
                if temperature < settings.MAX_TEMP:
                    door.people_inside.add(worker)
                    door.sanitizer_perc = sanitizer_perc
                    door.save()
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

def update_logtime(log):
    log.exit_datetime = datetime.now()
    log.save()
    return JsonResponse({                                                                                                       #En caso de que no exista un trabajador con ese codigo de tarjeta o una puerta con esa mac devuelve una respuesta en formato JSON de que no le esta permitido ingresar
        'error_message': None,
        'success_message': 'DateTime Updated',
    })

def init(request):
    pass

@csrf_exempt
def verify(request):
    
    if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):
        
        code = request.POST['code']                                                                                                     #Se guarda la informacion enviada por la raspberry en variables   
        temperature = float(request.POST.get('temperature', 0))                                                                         #Se guarda la informacion enviada por la raspberry en variables
        facemask = request.POST.get('facemask')                                                                                         #Se guarda la informacion enviada por la raspberry en variables
        mac = request.POST['mac']      
        sanitizer_perc = request.POST.get('sanitizer_perc')                                                                                 #Se guarda la informacion enviada por la raspberry en variables

        try:
            worker = Worker.objects.get(card_code=code, is_active=True)                                                                 #Intenta obtener el objeto del trabajador que tenga la misma card code 
            door = Door.objects.get(mac=mac, is_active=True)                                                                                            #Intenta obtener el objeto de la puerta que tenga la misma mac que la raspberry que envio el POST

            log = Logs.objects.filter(worker_id=worker, door_id=door, exit_datetime=None, authorized=True)
            log_exists = log.exists()

            if log_exists:
                door.people_inside.remove(worker)
                door.save()
                return update_logtime(log[0])
            else:
                if facemask == 'true' and temperature < settings.MAX_TEMP:                                                              #Se fija si el trabajador tiene el barbijo bien puesto y una temperatura menor a 37
                    return save_log(request, worker, door, facemask, temperature, sanitizer_perc, 'true')                               #Envia los datos dentro del parentesis a la funcion save_log y devuelve lo que devuelva esa funcion
                else:                                                                                                                   #En caso con no cumplir las condiciones del if ingresa aca
                    return save_log(request, worker, door, facemask, temperature, None, 'false')                                              #Envia los datos dentro del parentesis a la funcion save_log y devuelve lo que devuelva esa funcion


        except ObjectDoesNotExist:
            return JsonResponse({                                                                                                       #En caso de que no exista un trabajador con ese codigo de tarjeta o una puerta con esa mac devuelve una respuesta en formato JSON de que no le esta permitido ingresar
                'error_message': 'Not allowed',
                'success_message': None,
            })
        except Exception as e:
            return JsonResponse({                                                                                                       #Envia la informacion en formato JSON de que hubo un error
                'error_message': f'Error: {e}',
                'success_message': None,
            })
    else:
        return HttpResponseForbidden()

def env_update(request):
    pass