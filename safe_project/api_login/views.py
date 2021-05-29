import os
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from api_tables.models import User
# Create your views here.

@csrf_exempt
def login(request):
    if request.method == 'POST':
        if request.POST.get('SECRET_KEY') and request.POST['SECRET_KEY'] == os.environ.get("SECRET_KEY"):
            try:
                username = User.objects.get(
                    Q(
                        Q(username = request.POST["identifier"]) |
                        Q(email = request.POST["identifier"]) |
                        Q(phone_number = request.POST["identifier"])
                    ) & 
                    Q(is_active = True)
                ).username

                password = request.POST["password"] 

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    return JsonResponse({
                        'authorized': 'true',
                        'user_id': user.id,
                        'error_message': None,
                        'success_message': 'Succesfully logged in.'
                    })
                else:
                    return JsonResponse({
                        'authorized': 'false',
                        'user_id': None,
                        'error_message': 'Incorrect Password.',
                        'success_message': None
                    })

            except ObjectDoesNotExist:
                return JsonResponse({
                        'authorized': 'false',
                        'user_id': None,
                        'error_message': 'Could not find a user with those credentials.',
                        'success_message': None
                    })
            except Exception as e:
                return JsonResponse({
                        'authorized': 'false',
                        'user_id': None,
                        'error_message': f'Error: {e}',
                        'success_message': None
                    })
        else:
            return HttpResponseForbidden()

def verify(request):
    pass