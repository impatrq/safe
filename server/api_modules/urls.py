from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init),
    path('verify/', views.verify),
    path('env_update/', views.env_update),
]