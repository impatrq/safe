from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init),
    path('verify/', views.verify),
    path('env_update/', views.env_update),
    path('get_door_status/', views.get_door_status),
    path('main_door_update/', views.main_door_update),
]