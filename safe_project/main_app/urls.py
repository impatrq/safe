from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="main-index"),
    path('login/', views.login, name="main-login"),
    path('logout/', views.logout, name="main-logout"),
]