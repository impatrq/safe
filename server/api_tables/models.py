from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#TODO Agregar al modelo Logs los campos de ambiente seguro y ventilado (Boolean)

class User(AbstractUser): 
    username = models.CharField('username', max_length=64, blank=False, null=False, unique=True,
        error_messages={
            'unique': "Ya existe un usuario con este nombre de usuario.",
        })
    token = models.CharField('Token', max_length=7, null=False, blank=False)
    first_name = models.CharField('first name', max_length=64, blank=False, null=False)
    last_name = models.CharField('last name', max_length=64, blank=False, null=False)
    email = models.EmailField('email address', unique=True, blank=False, null=False,
        error_messages={
            'unique': "Ya existe un usuario con este email.",
        })
    phone_number = models.CharField('phone number', unique=True, max_length=20, blank=False, null=False,
        error_messages={
                'unique': "Ya existe un usuario con este número de teléfono.",
            })
    company_name = models.CharField('company name', max_length=64)
    company_address = models.CharField('company adress', max_length=64)
    is_active = models.BooleanField('is active', default= True, editable= True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'phone_number', 'company_name', 
        'company_address']

class Logs(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=False, blank=False)
    worker_id = models.ForeignKey('Worker', on_delete=models.CASCADE, null=False, blank=False)
    door_id = models.ForeignKey('Door', on_delete=models.CASCADE, null=False, blank=False)
    entry_datetime = models.DateTimeField('Entry DateTime', auto_now=False, auto_now_add=True)
    exit_datetime = models.DateTimeField('Exit DateTime', auto_now=False, auto_now_add=False, null=True, blank=True)
    facemask = models.BooleanField('Facemask', blank=False, null=False)
    temperature = models.CharField('Temperature', max_length=8, blank=False, null=False)
    authorized = models.BooleanField('Authorized', blank=False, null=False)
    worker_image =  models.ImageField('worker image', upload_to='logs_images/', height_field=None, width_field=None, max_length=None)
    is_active = models.BooleanField('Is Active', default=True)

    def __str__(self):
        entry_datetime = datetime.strftime(self.entry_datetime, "%Y/%m/%dat%H:%M:%S")
        if self.exit_datetime:
            exit_datetime = datetime.strftime(self.exit_datetime, "%Y/%m/%dat%H:%M:%S")
        else:
            exit_datetime = None

        return f'{self.worker_id.last_name}-{entry_datetime}-{exit_datetime}'

class Door(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    mac = models.CharField('MAC', max_length=64, blank=False, null=False)
    sector_name = models.CharField('Sector Name', max_length=64, blank=False, null=False)
    door_name = models.CharField('Door Name', max_length=64, blank=False, null=False)
    is_opened = models.BooleanField('Is Opened', default=False)
    date_created = models.DateTimeField('Date Created', blank=False, null=False, auto_now=False, auto_now_add=True)
    people_inside = models.ManyToManyField('Worker', blank=True, null=True)
    sanitizer_perc = models.CharField('Sanitizer Percentage', max_length=8, blank=False, null=False)
    is_active = models.BooleanField('Is Active', default=True)

    _co2_level = models.FloatField('CO2 Level', blank=True, null=True)
    _co_level = models.FloatField('CO Level', blank=True, null=True)
    _metano_level = models.FloatField('Metano Level', blank=True, null=True)
    _lpg_level = models.FloatField('lpg Level', blank=True, null=True)

    #TODO investigtar los valores que determinan si es seguro o no
    @property
    def is_safe(self):
        if(self._co2_level < 700 and self._co_level < 50 and self._metano_level < 100 and self._lpg_level < 100):
            return True
        else:
            return False
           

    def update_env(self, co2_level, co_level, metano_level, lpg_level):
        self._co2_level = co2_level
        self._co_level = co_level
        self._metano_level = metano_level
        self._lpg_level = lpg_level

    @property
    def get_gases_values(self):
        return {'co2_level': self._co2_level, 'co_level': self._co_level, 'metano_level': self._metano_level, 'lpg_level': self._lpg_level}

    def __str__(self):
        return f"{self.sector_name} - {self.door_name}"

class Worker(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    first_name = models.CharField('First Name', max_length=64, blank=False, null=False)
    last_name = models.CharField('Last Name', max_length=64, blank=False, null=False)
    phone_number = models.CharField('Phone Number', max_length=20, blank=False, null=False)
    email = models.EmailField('Email', blank=False, null=False)
    address = models.CharField('Address', max_length=64, blank=False, null=False)
    card_code = models.CharField('Card Code', max_length=64, blank=False, null=False)
    worker_image = models.ImageField('worker image', upload_to='workers_images/', height_field=None, width_field=None, max_length=None)
    date_created = models.DateTimeField('Date Created', blank=False, null=False, auto_now=False, auto_now_add=True)
    is_active = models.BooleanField('Is Active', default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
