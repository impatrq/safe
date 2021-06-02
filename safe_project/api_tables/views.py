import json
import os
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import User, Logs, Worker, Door
from .forms import UserForm, LogsForm, WorkerForm, DoorForm, EditWorkerForm

# Create your views here.
# TODO revisar si el eliminado sigue siendo logico o no y ver si cambiar el is_active en el update

#Tods los comentarios hechos en la parte de USERS son similares en las demas partes

# USERS

def read_users(request):
    if request.GET.get('sk') == os.environ.get('SECRET_KEY'):

        try:
            response = dict()

            users_list = User.objects.all()
            # users_list = User.objects.filter(is_active=True)

            paginator = Paginator(users_list, 1)

            page = paginator.page(request.GET.get('page', 1))

            if page.has_next():
                response['next_page'] = page.next_page_number()
            if page.has_previous():
                response['prev_page'] = page.previous_page_number()

            response['results'] = serialize('json', page.object_list)
            response['num_pages'] = paginator.num_pages

            response['media_path'] = settings.CURRENT_HOST + '/media/'

            return JsonResponse({
                'error_message': None,
                'success_message': 'Successfully fetched.',
                'data': response
            })
        except Exception as e:
            return JsonResponse({
                'error_message': f'Error: {e}',
                'success_message': None,
            })

    else:
        return HttpResponseForbidden()

@csrf_exempt
def create_users(request):
    if request.method == 'POST':                                                                               #Se fija si se le hizo un POST a la URL correspondiente a esta vista
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):

                                                                                                                #Busca si ya existe un usuario creado con el mismo username, email o telefono. 
                                                                                                                #Y devulve True si existe y False si no existe 
            user_exists = User.objects.filter(
                Q(username=request.POST["username"]) |
                Q(email=request.POST["email"]) |
                Q(phone_number=request.POST["phone_number"])
            ).exists() 

            if not user_exists:                                                                                 #Se fija si el usuario no existe 
                form = UserForm(request.POST)                                                                   #Crea un formulario con la informacion del usuario que se quiere crear
                if form.is_valid():                                                                             #Se fija si el formulario es valido 
                    user = form.save()                                                                          #Si es valido guarda el formulario con la infromacion enviada 
                    user.set_password(request.POST['password'])                                                 #Se establece la contraseña que se indico al crear el usuario
                    user.save()                                                                                 #Se guarda el usuario con su contraseña
                    
                    return JsonResponse({                                                                       #Envia la informacion en formato JSON de que se registro el usuario
                        'error_message': None,
                        'success_message': 'Succesfully registered.'
                    })
                else:
                    return JsonResponse({                                                                       #Envia la informacion en formato JSON de que el formulario no es valido
                        'error_message': f'Form is not valid.',
                        'success_message': None
                    })
            else:
                return JsonResponse({                                                                           #Envia la informacion en formato JSON de que ya existe un usuario con esos datos
                    'error_message': 'User with some of those credentials already exists.',
                    'success_message': None
                })

        else:
            return HttpResponseForbidden()

@csrf_exempt
def update_users(request, id):
    if request.method == 'POST':                                                                                 #Se fija si se le hizo un POST a la URL correspondiente a esta vista
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):

            try: 
                user = User.objects.get(pk=id)                                                                   #Se intenta obtener algun usuario que coincida con el id que se envio por la URL. pk es otra forma de referirse al id    

                form = UserForm(request.POST, instance=user)                                                     #Crea un formulario con la informacion del usuario que se desea actualizar. El instance=user indica que es una instancia asi que no intenta crear otro usuario con una informacion parecida 
                if form.is_valid():                                                                              #Se fija si el formulario es valido 
                    form.save()                                                                                  #Si es valido guarda el formulario con la infromacion enviada 
                    return JsonResponse({                                                                        #Envia la informacion en formato JSON de que se actualizo el usuario
                        'error_message': None,
                        'success_message': 'Succesfully updated.'
                    })
                else:
                    return JsonResponse({                                                                        #Envia la informacion en formato JSON de que el formulario no es valido
                        'error_message': f'Form is not valid. {form.errors}',
                        'success_message': None
                    })
            except ObjectDoesNotExist:
                return JsonResponse({                                                                            #Envia la informacion en formato JSON de que no existe un usuario con esa ip
                    'error_message': f'Object with id {id} does not exist.',
                    'success_message': None
                })
            except Exception as e:
                return JsonResponse({                                                                            #Envia la informacion en formato JSON de que hubo un error
                    'error_message': f'Error: {e}',
                    'success_message': None
                })

        else:
            return HttpResponseForbidden()

@csrf_exempt
def delete_users(request, id):
    if request.method == 'POST':
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):

            try:
                user = User.objects.get(pk=id)                                                                    #Se intenta obtener algun usuario que coincida con el id que se envio por la URL    
                user.is_active = False                                                                            #Si obtiene algun usuario que coincida cambia el estado de actividad como False (eliminado logico) 
                user.save()                                                                                       #Guarda el usuario con el estado de actividad cambiado

                return JsonResponse({                                                                             #Envia la informacion en formato JSON de que se elimino el usuario exitosamente
                    'error_message': None,
                    'success_message': 'Succesfully deleted.'
                })
            except ObjectDoesNotExist:
                return JsonResponse({                                                                             #Envia la informacion en formato JSON de que no existe un objeto con esa id
                    'error_message': f'Object with id {id} does not exist.',
                    'success_message': None
                })
            except Exception as e:
                return JsonResponse({                                                                             #Envia la informacion en formato JSON de que hubo un error al intentar elimar
                    'error_message': f'Error: {e}',
                    'success_message': None
                })

        else:
            return HttpResponseForbidden()

# LOGS

def read_logs(request):
    if request.GET.get('sk') == os.environ.get('SECRET_KEY'):

        try:
            response = dict()

            logs_list = Logs.objects.all()

            paginator = Paginator(logs_list, 1)

            page = paginator.page(request.GET.get('page', 1))

            if page.has_next():
                response['next_page'] = page.next_page_number()
            if page.has_previous():
                response['prev_page'] = page.previous_page_number()

            response['results'] = serialize('json', page.object_list)
            response['num_pages'] = paginator.num_pages

            response['media_path'] = settings.CURRENT_HOST + '/media/'

            return JsonResponse({
                'error_message': None,
                'success_message': 'Successfully fetched.',
                'data': response
            })
        except Exception as e:
            return JsonResponse({
                'error_message': f'Error: {e}',
                'success_message': None,
            })

    else:
        return HttpResponseForbidden()

@csrf_exempt
def create_logs(request):
    if request.method == 'POST':
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):
            form = LogsForm(request.POST, request.FILES)
            if form.is_valid():
                log = form.save()
                return JsonResponse({
                    'error_message': None,
                    'success_message': 'Succesfully registered.'
                })
            else:
                return JsonResponse({
                    'error_message': f'Form is not valid. {form.errors}',
                    'success_message': None
                })
        else:
            return HttpResponseForbidden()

@csrf_exempt
def update_logs(request, id):
    if request.method == 'POST':
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):
            try:
                log = Logs.objects.get(pk=id)

                form = LogsForm(request.POST, request.FILES, instance=log)
                if form.is_valid():
                    form.save()
                    return JsonResponse({
                        'error_message': None,
                        'success_message': 'Succesfully updated.'
                    })
                else:
                    return JsonResponse({
                        'error_message': f'Form is not valid. {form.errors}',
                        'success_message': None
                    })
            except ObjectDoesNotExist:
                return JsonResponse({
                    'error_message': f'Object with id {id} does not exist.',
                    'success_message': None
                })
            except Exception as e:
                return JsonResponse({
                    'error_message': f'Error: {e}',
                    'success_message': None
                })

        else:
            return HttpResponseForbidden()

@csrf_exempt
def delete_logs(request, id):
    if request.method == 'POST':
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):

            try:
                log = Logs.objects.get(pk=id)
                log.is_active = False
                log.save()

                return JsonResponse({
                    'error_message': None,
                    'success_message': 'Succesfully deleted.'
                })

            except ObjectDoesNotExist:
                return JsonResponse({
                    'error_message': f'Object with id {id} does not exist.',
                    'success_message': None
                })
            except Exception as e:
                return JsonResponse({
                    'error_message': f'Error: {e}',
                    'success_message': None
                })

        else:
            return HttpResponseForbidden()

# DOORS

def read_doors(request):
    if request.GET.get('sk') == os.environ.get('SECRET_KEY'):

        try:
            response = dict()

            doors_list = Door.objects.all()

            paginator = Paginator(doors_list, 1)

            page = paginator.page(request.GET.get('page', 1))

            if page.has_next():
                response['next_page'] = page.next_page_number()
            if page.has_previous():
                response['prev_page'] = page.previous_page_number()

            response['results'] = serialize('json', page.object_list)
            response['num_pages'] = paginator.num_pages

            response['media_path'] = settings.CURRENT_HOST + '/media/'

            return JsonResponse({
                'error_message': None,
                'success_message': 'Successfully fetched.',
                'data': response
            })
        except Exception as e:
            return JsonResponse({
                'error_message': f'Error: {e}',
                'success_message': None,
            })

    else:
        return HttpResponseForbidden()

@csrf_exempt
def create_doors(request):
    if request.method == 'POST':
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):

            door_exists = Door.objects.filter(mac=request.POST['mac']).exists()

            if not door_exists:
                form = DoorForm(request.POST)
                if form.is_valid():
                    door = form.save()
                    return JsonResponse({
                        'error_message': None,
                        'success_message': 'Succesfully registered.',
                    })
                else:
                    return JsonResponse({
                        'error_message': f'Form is not valid.',
                        'success_message': None
                    })
            else:
                return JsonResponse({
                    'error_message': 'Door with that MAC already exists.',
                    'success_message': None
                })
        else:
            return HttpResponseForbidden()

@csrf_exempt
def update_doors(request, id):
    if request.method == 'POST':
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):
            try:
                door = Door.objects.get(pk=id)

                form = DoorForm(request.POST, instance=door)
                if form.is_valid():
                    form.save()
                    return JsonResponse({
                        'error_message': None,
                        'success_message': 'Succesfully updated.'
                    })
                else:
                    return JsonResponse({
                        'error_message': f'Form is not valid. {form.errors}',
                        'success_message': None
                    })
            except ObjectDoesNotExist:
                return JsonResponse({
                    'error_message': f'Object with id {id} does not exist.',
                    'success_message': None
                })
            except Exception as e:
                return JsonResponse({
                    'error_message': f'Error: {e}',
                    'success_message': None
                })

        else:
            return HttpResponseForbidden()

@csrf_exempt
def delete_doors(request, id):
    if request.method == 'POST':
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):

            try:
                door = Door.objects.get(pk=id)
                door.is_active = False
                door.save()

                return JsonResponse({
                    'error_message': None,
                    'success_message': 'Succesfully deleted.'
                })
            except ObjectDoesNotExist:
                return JsonResponse({
                    'error_message': f'Object with id {id} does not exist.',
                    'success_message': None
                })
            except Exception as e:
                return JsonResponse({
                    'error_message': f'Error: {e}',
                    'success_message': None
                })

        else:
            return HttpResponseForbidden()

# WORKERS

def read_workers(request):
    if request.GET.get('sk') == os.environ.get('SECRET_KEY'):

        try:
            response = dict()

            workers_list = Worker.objects.all()

            paginator = Paginator(workers_list, 10)

            page = paginator.page(request.GET.get('page', 1))

            if page.has_next():
                response['next_page'] = page.next_page_number()
            if page.has_previous():
                response['prev_page'] = page.previous_page_number()

            response['results'] = serialize('json', page.object_list)
            response['num_pages'] = paginator.num_pages

            response['media_path'] = settings.CURRENT_HOST + '/media/'

            return JsonResponse({
                'error_message': None,
                'success_message': 'Successfully fetched.',
                'data': response
            })
        except Exception as e:
            return JsonResponse({
                'error_message': f'Error: {e}',
                'success_message': None,
            })

    else:
        return HttpResponseForbidden()

@csrf_exempt
def create_workers(request):
    if request.method == 'POST':
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):

            worker_exists = Worker.objects.filter(
                Q(email=request.POST['email']) |
                Q(phone_number=request.POST['phone_number']) |
                Q(card_code=request.POST['card_code'])
            ).exists()

            if not worker_exists:
                form = WorkerForm(request.POST, request.FILES)
                if form.is_valid():
                    worker = form.save()
                    return JsonResponse({
                        'error_message': None,
                        'success_message': 'Succesfully registered.',
                    })
                else:
                    return JsonResponse({
                        'error_message': f'Form is not valid. {form.errors}',
                        'success_message': None
                    })

            else:
                return JsonResponse({
                    'error_message': 'User with some of those credentials already exists.',
                    'success_message': None
                })
        else:
            return HttpResponseForbidden()

@csrf_exempt
def update_workers(request, id):
    if request.method == 'POST':
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get('SECRET_KEY'):
            try:
                worker = Worker.objects.get(pk=id)

                form = EditWorkerForm(request.POST, instance=worker)
                if form.is_valid():
                    form.save()
                    return JsonResponse({
                        'error_message': None,
                        'success_message': 'Succesfully updated.'
                    })
                else:
                    return JsonResponse({
                        'error_message': f'Form is not valid. {form.errors}',
                        'success_message': None
                    })
            except ObjectDoesNotExist:
                return JsonResponse({
                    'error_message': f'Object with id {id} does not exist.',
                    'success_message': None
                })
            except Exception as e:
                return JsonResponse({
                    'error_message': f'Error: {e}',
                    'success_message': None
                })

        else:
            return HttpResponseForbidden()
    else:
        worker = Worker.objects.get(pk=id)
        return JsonResponse({
            'error_message': None,
            'success_message': 'Edit Form Fetched Successfully',
            'data': render_to_string('forms/partial-worker-edit-form.html', {'form': EditWorkerForm(instance=worker), 'sk': os.environ.get('SECRET_KEY'), 'id': id})
        })

@csrf_exempt
def delete_workers(request, id):
    if request.method == 'POST':
        SECRET_KEY = json.loads(request.body.decode('utf-8'))['SECRET_KEY']
        if SECRET_KEY and SECRET_KEY == os.environ.get('SECRET_KEY'):

            try:
                worker = Worker.objects.get(pk=id)
                worker.is_active = False
                worker.save()

                return JsonResponse({
                    'error_message': None,
                    'success_message': 'Succesfully deleted.'
                })
            except ObjectDoesNotExist:
                return JsonResponse({
                    'error_message': f'Object with id {id} does not exist.',
                    'success_message': None
                })
            except Exception as e:
                return JsonResponse({
                    'error_message': f'Error: {e}',
                    'success_message': None
                })

        else:
            return HttpResponseForbidden()
