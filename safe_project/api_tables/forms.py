from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms import fields
from .models import User, Door, Worker, Logs

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'company_name', 
        'company_address']

class LogsForm(forms.ModelForm):
    class Meta:
        model = Logs
        fields = ['user_id', 'worker_id', 'door_id', 'facemask', 
        'temperature', 'authorized', 'worker_image']

class DoorForm(forms.ModelForm):
    class Meta:
        model = Door
        fields = ['user_id', 'mac', 'sector_name', 'door_name']

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['user_id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 
        'card_code', 'worker_image']

# EDIT FORMS

class EditWorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['user_id', 'first_name', 'last_name', 'phone_number', 'email', 'address', 
        'card_code']