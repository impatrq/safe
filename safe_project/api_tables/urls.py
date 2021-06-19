from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.read_users),
    path('users/create/', views.create_users),
    path('users/update/<int:id>/', views.update_users),
    path('users/delete/<int:id>/', views.delete_users),

    path('logs/', views.read_logs),
    path('logs/create/', views.create_logs),
    path('logs/update/<int:id>/', views.update_logs),
    path('logs/delete/<int:id>/', views.delete_logs),

    path('doors/', views.read_doors),
    path('doors/create/', views.create_doors),
    path('doors/update/<int:id>/', views.update_doors),
    path('doors/delete/<int:id>/', views.delete_doors),
    path('doors/all/', views.read_all_doors),
    path('doors/search/', views.search_doors),

    path('workers/', views.read_workers),
    path('workers/create/', views.create_workers),
    path('workers/update/<int:id>/', views.update_workers),
    path('workers/delete/<int:id>/', views.delete_workers),
    path('workers/search/', views.search_workers),

    path('doors/get_doors_status/', views.get_doors_info),

    path('report/', views.report),
]