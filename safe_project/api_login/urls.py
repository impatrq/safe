from collections import UserString
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('verify/', views.verify, name="verify"),
]