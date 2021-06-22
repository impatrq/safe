from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="main-index"),
    path('login/', views.login, name="main-login"),
    path('logout/', views.logout, name="main-logout"),
    path('workers/', views.workers, name="main-workers"),
    path('doors/', views.doors, name="main-doors"),
    path('logs/', views.logs, name="main-logs"),
]