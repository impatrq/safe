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

    # Obtenemos los datos de la imagen codificados y creamos el diccionario que le pasamos al request con el nombre de la foto formateado

    file = request.FILES['worker_image'].file.getvalue()                                                                                
    files = {'worker_image': (f'{worker.first_name}{worker.last_name}-{datetime.now().strftime("%Y-%m-%dat%H-%M-%S")}.png', file)}      

    response = requests.post(settings.CURRENT_HOST + '/api/tables/logs/create/', data=data, files=files)

    if response.status_code == 200:
        json_response = response.json()
        if json_response['error_message']:
            return JsonResponse(json_response)
        else:
            if facemask:
                if temperature < settings.MAX_TEMP:
                    # Se registra la persona dentro de la puerta y se la deja entrar
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
    # Se actualiza la salida de la persona en el log
    log.exit_datetime = datetime.now()
    log.save()
    return JsonResponse({                                                                                                       
        'error_message': None,
        'success_message': 'Allowed',
    })

@csrf_exempt
def init(request):
    
    if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):
        
        mac = request.POST.get('mac', '')

        try:
            
            door = Door.objects.get(mac=mac)

            return JsonResponse({
                'error_message': None,
                'success_message': 'Successfully fetched Token.',
                'token': door.user_id.token,
            })

        except ObjectDoesNotExist:
            
            return JsonResponse({
                'error_message': 'Door with that MAC was not found.',
                'success_message': None,
            })

    else:
        return HttpResponseForbidden()
    
@csrf_exempt
def verify(request):
    
    if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):
        

        # Se guarda la informacion enviada por la raspberry en variables

        code = request.POST['code']
        temperature = float(request.POST.get('temperature', 0))
        facemask = request.POST.get('facemask') == 'True'
        mac = request.POST['mac']
        sanitizer_perc = request.POST.get('sanitizer_perc')
        token = request.POST.get('token')             

        try:

            # Intenta obtener el objeto del trabajador que tenga la misma card code y la puerta que tenga esa mac 

            worker = Worker.objects.get(card_code=code, is_active=True, user_id__token=token)
            door = Door.objects.get(mac=mac, is_active=True, user_id__token=token)

            log = Logs.objects.filter(worker_id=worker, door_id=door, exit_datetime=None, authorized=True, user_id__token=token)
            log_exists = log.exists()

            if log_exists:
                door.people_inside.remove(worker)
                door.save()
                return update_logtime(log[0])
            else:
                # Verificamos si el trabajador tiene el barbijo bien puesto y una temperatura menor a 37 y registramos mediante save_log el intento de entrada o la entrada
                if facemask and temperature < settings.MAX_TEMP:                                       
                    return save_log(request, worker, door, facemask, temperature, sanitizer_perc, True)                          
                else:
                    return save_log(request, worker, door, facemask, temperature, None, False)                                        


        # En caso de que no exista un trabajador con ese codigo de tarjeta o una puerta con esa mac devuelve una respuesta en formato JSON de que no le esta permitido ingresar
        except ObjectDoesNotExist:
            return JsonResponse({                                                                                                       
                'error_message': 'Not allowed',
                'success_message': None,
            })
        # Enviamos la informacion en formato JSON de que hubo un error
        except Exception as e:
            return JsonResponse({                                                                                                       
                'error_message': f'Error: {e}',
                'success_message': None,
            })
    else:
        return HttpResponseForbidden()

@csrf_exempt
def env_update(request):
    data = json.loads(request.body.decode('utf-8'))
    if data.get('SECRET_KEY') and data['SECRET_KEY'] == os.environ.get('SECRET_KEY'):

        door_mac = data['door_mac']                                                             # Obtenemos el mac de la puerta que nos llego
        co2_level = float(data['co2_level'])                                                    # Obtenemos el nivel de co2 que nos llego
        co_level = float(data['co_level'])                                                      # Obtenemos el nivel de co que nos llego
        metano_level = float(data['metano_level'])                                              # Obtenemos el nivel de metano que nos llego
        lpg_level = float(data['lpg_level'])                                                    # Obtenemos el nivel de lpg que nos llego
    
        try:                                
            door = Door.objects.get(mac=door_mac)                                                       #Obtenemos la instancia del objeto al que corresponda ese mac

            door.update_env(int(co2_level), int(co_level), int(metano_level), int(lpg_level))                               #Guardamos los valores de los sensores en servidor 

            door.save()

            # Enviamos la informacion en formato JSON de que todo salio bien y los valores de cada gas
            return JsonResponse({                                                                                                       
                'error_message': None,
                'success_message': 'Successfully Updated',
                'is_safe': door.is_safe,
                'co2_level': get_gases_level(door.get_gases_values['co2_level'], 600, 700, 10000),
                'co_level': get_gases_level(door.get_gases_values['co_level'], 120, 185, 10000),
                'metano_level': get_gases_level(door.get_gases_values['metano_level'], 300, 1300, 10000),
                'lpg_level': get_gases_level(door.get_gases_values['lpg_level'], 450, 1300, 10000),
            })

        # Enviamos la informacion en formato JSON de que hubo un error
        except Exception as e:
            return JsonResponse({                                                                                                       
                'error_message': f'Error: {e}',
                'success_message': None,
            })
    else:
        return HttpResponseForbidden()

def get_door_status(request):

    if request.GET.get('sk') and request.GET['sk'] == os.environ.get('SECRET_KEY'):
        
        mac = request.GET.get('mac', '')

        try:
            
            door = Door.objects.get(mac=mac)

            return JsonResponse({                                                                                                       
                'error_message': None,
                'success_message': 'Successfully Fetched Door Data',
                'people_inside': door.people_inside.count(),
                'sanitizer_perc': door.sanitizer_perc,
                'is_safe': door.is_safe,
                'co2_level': get_gases_level(door.get_gases_values['co2_level'], 600, 700, 10000),
                'co_level': get_gases_level(door.get_gases_values['co_level'], 120, 185, 10000),
                'metano_level': get_gases_level(door.get_gases_values['metano_level', 300, 1300, 10000]),
                'lpg_level': get_gases_level(door.get_gases_values['lpg_level'], 450, 1300, 10000),

            })

        except ObjectDoesNotExist:
            
            return JsonResponse({
                'error_message': 'Door with that MAC was not found.',
                'success_message': None,
            })

    else:
        return HttpResponseForbidden()

@csrf_exempt
def main_door_update(request):

    if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):

        mac = request.POST.get('mac')
        token = request.POST.get('token')
        is_opened = request.POST.get('is_opened')

        try:

            door = Door.objects.get(mac=mac, is_active=True, user_id__token=token)

            door.is_opened = is_opened

            door.save()

            return JsonResponse({                                                                                                       
                'error_message': None,
                'success_message': 'Successfully updated Door status',
            })

        except ObjectDoesNotExist:
            return JsonResponse({                                                                                                       
                'error_message': 'Door does not exist.',
                'success_message': None,
            })
            
        except Exception as e:
            return JsonResponse({                                                                                                       
                'error_message': f'Error: {e}',
                'success_message': None,
            })

    else:
        return HttpResponseForbidden()

# Extra functions

def get_gases_level(gas_value, low, medium, high):
    if (gas_value > 0 and gas_value < low):
        return "Low" 
    elif (gas_value > low and gas_value < medium):
        return "Medium" 
    elif (gas_value > medium and gas_value < high):
        return "High"