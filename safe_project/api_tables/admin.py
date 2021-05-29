from django.contrib import admin
from .models import User, Worker, Logs, Door

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'phone_number', 'company_name', 'email', 'is_active']

class LogsAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'worker_id', 'door_id', 'facemask', 'temperature', 'authorized', 'is_active']
    readonly_fields = ['entry_datetime']

class DoorAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'mac', 'sector_name', 'door_name', 'is_active']
    readonly_fields = ['date_created']

class WorkerAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 'card_code', 'is_active']
    readonly_fields = ['date_created']

admin.site.register(User, UserAdmin)
admin.site.register(Logs, LogsAdmin)
admin.site.register(Door, DoorAdmin)
admin.site.register(Worker, WorkerAdmin)