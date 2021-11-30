from datetime import datetime, timedelta
import json
import re
import numpy
from numpy.core.fromnumeric import var
import requests
import configparser
import time
from apscheduler.schedulers.background import BackgroundScheduler
import os
import shutil

from tensorflow.python import util
from getmac import get_mac_address as gma

#from src.repeatedTimer import RepeatedTimer
import src.detect_mask as ai
import src.take_photos as ph
import src.qr_generator as qr
import src.supp as supp

FILE_DIR = os.path.dirname(__file__) + '/'

class Data:
    def __init__(self, host , init , verify , get_door_status , main_door_update , secret_key):

        # * ▼ WEB DATA VARIABLES ▼
        self.url = host
        self.url_init = self.url + init
        self.url_verify = self.url + verify
        self.url_get_door_status = self.url + get_door_status
        self.url_main_door_update = self.url + main_door_update

        self.secret_key = secret_key

        self.token = str()
        self.mac = gma()
        #self.mac = str()

        # * ▼ DOOR DATA VARIABLES ▼
        self.people_inside = str()
        self.is_safe = str()
        self.co2_level = str()
        self.co_level = str()
        self.ch4_level = str()
        self.lpg_level = str()

        self.is_safe_color = str()
        self.co2_color = str()
        self.co_color =  str()
        self.ch4_color = str()
        self.lpg_color = str()

        # * ▼ WORKER DATA VARIABLES ▼
        self.allowed = bool()
        self.code = str()
        self.face_mask = bool()
        self.face_mask_image = str()

        self.reason = str()

        self.first_name = str()
        self.last_name = str()
        self.worker_image = str()
        
        # * ▼ MICRO DATA VARIABLES ▼
        self.led_color = str()
        self.temperature = str()
        self.dispenser_percentage = str()
        self.joining = bool()
        self.door_is_opened = bool()
        self.time = int()

        # * ▼ NECESSARY DATA VARIABLES ▼
        self.stage = numpy.full(4, False)
        self.config = configparser.ConfigParser()
        self.s = BackgroundScheduler()
        self.s.start()
        self.info_type_data = dict()
        self.status = str()
        self.active = bool()

    def start(self):
        self.status = "CARGANDO..."
        self.showInfo("Loading")
        time.sleep(2)
        self.config.read(FILE_DIR + "config/settings.cfg")
        if self.config.getboolean("START","needtoken"):
            self.active = False
            qr_image = qr.generate(self.mac)
            save = FILE_DIR + "server/public/static/qr/qr_safe.png"
            shutil.copyfile(qr_image, save)
            self.showInfo("NeedToken")
            self.getToken()
            self.s.add_job(self.getToken,  "interval", seconds = 10)   
        else:
            self.active = True
            self.token = self.config["START"]["token"]
            self.getDoorInfo()
            self.s.add_job(self.getDoorInfo, "interval", seconds = 60)
    
    def getToken(self):
        if self.sendData2Web("init"): 
            self.s.remove_all_jobs()
            self.config.set("START", "needtoken", "false")
            self.config["START"]["token"] = self.token
            with open(FILE_DIR + 'config/settings.cfg', 'w') as configfile:
                self.config.write(configfile) 
                configfile.close()  
            self.getDoorInfo()
            self.s.add_job(self.getDoorInfo, "interval", seconds = 60)
            
               
    def getDoorInfo(self):
        r = requests.get(self.url_get_door_status + "?sk=" + self.secret_key + "&mac=" + self.mac) # * Request WEB
        if r.status_code == 200:
            response_dict = r.json()
            if not response_dict['error_message']:
                self.people_inside = str(response_dict['people_inside'])
                self.is_safe = "SEGURO" if response_dict['is_safe'] else "NO SEGURO"  
                self.co2_level = response_dict['co2_level']
                self.co_level = response_dict['co_level']
                self.ch4_level = response_dict['metano_level']
                self.lpg_level = response_dict['lpg_level']

                self.co2_color = supp.whatColor(self.co2_level)
                self.co_color = supp.whatColor(self.co_level)
                self.ch4_color = supp.whatColor(self.ch4_level)
                self.lpg_color = supp.whatColor(self.lpg_level)
                self.is_safe_color = supp.whatColor(self.is_safe)
            self.showInfo("Default")

    def analize(self, dictionary): 
        if self.active:
            if dictionary.get("code"):
                self.code = dictionary["code"]
                self.joining = dictionary["joining"]
                if self.joining:
                    self.stage[0] = True
                    self.s.remove_all_jobs()
                    self.showInfo("How2UseTemp")
                else:
                    self.sendData2Web("mini_verify")
                    return True

            elif dictionary.get("temperature"):
                self.temperature = dictionary["temperature"]
                if self.stage[0]:
                    self.stage[1] = True
                    self.showInfo("Temp")
                    time.sleep(3)
                    self.showInfo("How2UseDisp")
                else:
                    self.s.remove_all_jobs()
                    self.showInfo("Temp")
                    time.sleep(3)
                    self.showInfo("Default")
                    self.s.add_job(self.getDoorInfo, "interval", seconds = 60)

            elif dictionary.get("dispenser_percentage"):
                self.dispenser_percentage = dictionary["dispenser_percentage"]
                if self.stage[0]:
                    self.stage[2] = True
                    self.showInfo("Disp")
                    time.sleep(3)
                    self.showInfo("How2UseAI")
                else:
                    self.s.remove_all_jobs()
                    self.showInfo("Disp")
                    time.sleep(3)
                    self.showInfo("Default")
                    self.s.add_job(self.getDoorInfo, "interval", seconds = 60)
            
            elif dictionary.get("door_is_opened") is not None:
                self.door_is_opened = dictionary["door_is_opened"] == 1
                print(self.door_is_opened)
                self.sendData2Web("main_door_update")
            else:
                pass # ! NOT THE MOST FUCKING IDEA
            
            if numpy.all(self.stage[0:3]):
                time.sleep(2)
                self.status = "DETECTANDO BARBIJO..."
                self.showInfo("Loading")
                self.aiProcess()
                self.sendData2Web("verify")
                return True
    
    def aiProcess(self):
        ph.takePhotos(7)
        output = ai.process_images()
        print(output)
        file_image = output['average']['file']
        save = FILE_DIR + "server/public/static/img/face_mask.jpeg"
        shutil.copyfile(file_image, save)
        self.face_mask_image = FILE_DIR + "server/public/static/img/face_mask.jpeg"
        self.face_mask = output['average']['result']

    def sendData2Web(self, UrlTpye):
        if UrlTpye == "verify":
            values = {'SECRET_KEY': self.secret_key,
                        'token': self.token,
                        'code': self.code,
                        'temperature': self.temperature,
                        'facemask': self.face_mask,
                        'mac': self.mac,
                        'sanitizer_perc': self.dispenser_percentage}

            files = {'worker_image': open(self.face_mask_image,'rb')}
            print(self.url_verify)
            print(values)
            print(files)
            r = requests.post(self.url_verify, files=files, data=values) # * Request WEB
            print(r.status_code)
            if r.status_code == 200:
                response_dict = r.json()
                print(response_dict)
                if not response_dict["error_message"]:
                    worker_list = json.loads(response_dict["worker"])
                   
                    worker = worker_list[0]["fields"]
                    self.worker_image = response_dict["worker_image"]
                    self.first_name = worker["first_name"]
                    self.last_name = worker["last_name"]
                    self.allowed = True
                    self.led_color = "Green"
                    self.time = 4 
                    self.s.remove_all_jobs()
                    self.showInfo("AccessAllowed")
                    #self.s.add_job(self.getDoorInfo, "date", run_date= datetime.now() + timedelta(seconds = 4))
                    self.s.add_job(self.getDoorInfo, "interval", seconds = 60)
                else:
                    self.reason = response_dict["error_message"]
                    self.allowed = False
                    self.led_color = "Red"
                    self.time = 4
                    self.s.remove_all_jobs()
                    self.showInfo("AccessDenied")
                    #self.s.add_job(self.getDoorInfo, "date", run_date= datetime.now() + timedelta(seconds = 4))
                    self.s.add_job(self.getDoorInfo, "interval", seconds = 60)

                    
                self.stage[0] = False
                self.stage[1] = False
                self.stage[2]= False
            else:
                print(r.status_code)

        elif UrlTpye == "mini_verify":
            values = {'SECRET_KEY': self.secret_key,
                        'token': self.token,
                        'code': self.code,
                        'mac': self.mac}
            r = requests.post(self.url_verify, data=values) # * Request WEB
            print(r.status_code)
            if r.status_code == 200:
                response_dict = r.json()
                print(response_dict)
                if not response_dict["error_message"]:
                    self.allowed = True
                    self.led_color = "Green"
                    self.time = 4 
                else:
                    self.allowed = False
                    self.led_color = "Red"
                    self.time = 4
        
        elif UrlTpye == "init":
            values = {'SECRET_KEY': self.secret_key,
                        'mac': self.mac}
            r = requests.post(self.url_init, data=values) # * Request WEB
            print(r.status_code)
            if r.status_code == 200:
                response_dict = r.json()
                print(response_dict)
                if response_dict["success_message"] == "Successfully fetched Token.":
                    self.token = response_dict["token"]
                    return True
                else:
                    return False
            else:
                return False

        elif UrlTpye == "main_door_update":
            values = {'SECRET_KEY': self.secret_key,
                        'token': self.token,
                        'mac': self.mac,
                        'is_opened': self.door_is_opened}
            r = requests.post(self.url_main_door_update, data=values) # * Request WEB
            if r.status_code == 200:
                response_dict = r.json()
                if response_dict["success_message"] == "Successfully fetched Token.":
                    self.token = response_dict["token"]
                    return True     
        else:
            values = {'SECRET_KEY': self.secret_key,
                        'token': 'hkaAJD2',
                        'code': '0009712004',
                        'temperature': self.temperature,
                        'facemask': self.prueba,
                        'mac': "3",
                        'sanitizer_perc': self.dispenser_percentage}

            files = {'worker_image': open("ironman.jpg",'rb')}
            r = requests.post("http://192.168.1.110:8000/api/modules/verify/", files=files, data=values) # * Request WEB
            if r.status_code == 200:
                print(r.data)
                response_dict = r.json()
                if response_dict["success_message"] == "Allowed":
                    self.allowed = True
                    self.led_color = "green"
                    self.showInfo("AccessAllowed")
                    pass # TODO: Preparar respuesta
                else:
                    self.allowed = False
                    self.led_color = "red"
                    pass # TODO: Show NOT Allowd Info
                self.stage[0] = False
                self.stage[1] = False
                self.stage[2]= False
                print(response_dict)
            else:
                print(r.status_code)
            pass # TODO: Http request for the other cases
    
    def sendData2Micro(self, needData = None): # TODO: Fix variable response
        
        dict_response = {'allowed':self.allowed,
                            'time': self.time,
                            'joinning': self.joining,
                            'led_color':self.led_color}

        string_response = json.dumps(dict_response) + "\n"
        return string_response.encode()

    def showInfo(self, InfoType):   # * Info Types: - Default ✓
                                    # *             - Card ✓
                                    # *             - Only Temp ✓
                                    # *             - Only Dis% ✓
                                    # *             - Access allowed ✓
                                    # *             - Access denied ✓
                                    # ?             - Error Screen
                                    # ?             - Config
                                    # *                 > Need Token (QR page) ✓
                                    # ?                 > Pairing Mode
                                    # ?                 > WiFi Settings
                                    # ?                 > Factory Restoration
        with open(FILE_DIR + 'config/info_types_data.json') as json_file:
            self.info_type_data = json.load(json_file)
            json_file.close()
        file_name = self.info_type_data[InfoType].get('file')
        print(file_name)
        new_content = ""
        with open(FILE_DIR + f'server/templates/{file_name}', 'r') as file:
            content = file.read()
            for variable in self.info_type_data[InfoType]['variables']:
                content = content.replace(variable , getattr(vars()["self"], self.info_type_data[InfoType]['variables'][variable]))
            new_content = content
            file.close()
        with open(FILE_DIR + f'server/public/index.html', 'w') as file:
            file.write(new_content)
            file.close()
    



    
