import json
import numpy
import requests
import configparser
import sched, time
from getmac import get_mac_address as gma

import src.detect_mask as ai
import src.take_photos as ph
import src.qr_generator as qr

class Data:
    def __init__(self, url , init , verify , get_door_status , secret_key):

        # * ▼ WEB DATA VARIABLES ▼
        self.url = url
        self.url_init = self.url + init
        self.url_verify = self.url + verify
        self.url_get_door_status = self.url + get_door_status

        self.secret_key = secret_key

        self.token = str()
        self.mac = gma()
        #self.mac = str()

        # * ▼ DOOR DATA VARIABLES ▼
        self.people_inside = int()
        self.is_safe = bool()
        self.co2_level = str()
        self.co_level = str()
        self.metano_level = str()
        self.lpg_level = str()

        # * ▼ WORKER DATA VARIABLES ▼
        # ! self.email = str()
        self.allowed = bool()
        self.code = str()
        self.face_mask = bool()
        self.face_mask_image = str()
        
        # * ▼ MICRO DATA VARIABLES ▼
        self.led_color = str()
        self.temperature = str()
        self.dispenser_percentage = str()
        self.joining = bool()
        # ! self.dispenser = bool()
        # ! self.proximity_temp = bool()
        # ! self.proximity_dispenser = bool()


        self.prueba = True

        self.stage = numpy.full(4, False)

        self.config = configparser.ConfigParser()

        self.s = sched.scheduler(time.time, time.sleep)

        self.info_type_data = dict()

        #self.__dict__.update(dict1)

    def start(self):
        self.config.read("config/settings.cfg")
        if self.config["START"]["NeedToken"]:
            qr.generate(self.mac)
            self.showInfo("NeedToken")
            self.getToken()
        else:
            self.token = self.config["START"]["Token"]
            self.showInfo("Default")
    
    def getToken(self):
        if not self.sendData2Web("init"): 
            self.s.enter(10, 1 , self.getToken)   
            self.s.run()
        else:
            self.config["START"]["NeedToken"] = False
            self.config["START"]["Token"] = self.token
            with open('/config/settings.cfg', 'w') as configfile:
                self.config.write(configfile) 
                configfile.close()  
            self.getDoorInfo()

    def getDoorInfo(self):
        r = requests.get(self.url_get_door_status + "?sk=" + self.secret_key + "&mac=" + self.mac) # * Request WEB
        if r.status_code == 200:
            response_dict = r.json()
            if not response_dict['error_message']:
                self.people_inside = response_dict['people_inside']
                self.is_safe = response_dict['is_safe']
                self.co2_level = response_dict['co2_level']
                self.co_level = response_dict['co_level']
                self.metano_level = response_dict['metano_levell']
                self.lpg_level = response_dict['lpg_level']
        self.s.enter(60, 1 , self.getDoorInfo)   
        self.s.run()

    def analize(self, dictionary): 

        if dictionary.get("code"):
            self.code = dictionary["code"]
            self.joining = dictionary["joining"]
            self.stage[0] = True
            
            pass # TODO: Show Info

        elif dictionary.get("temperature"):
            self.temperature = dictionary["temperature"]
            if self.stage[0]:
                self.stage[1] = True
                pass # TODO: Show Info + Temp
            else:
                pass # TODO: Show Only Temp

        elif dictionary.get("dispenser"):
            self.dispenser = dictionary["dispenser"]
            self.dispenser_percentage = dictionary["dispenser_percentage"]
            if self.stage[0]:
                self.stage[2] = True
                pass # TODO: Show Info + Dispenser %
            else:
                pass # TODO: Show Dispenser %

        else:
            pass # ! NOT THE MOST FUCKING IDEA
        
        if numpy.all(self.stage[0:3]):
            ph.takePhotos(7)
            output = ai.process_images()
            print(output)
            self.sendData2Web(UrlTpye= False)     # TODO: Determine which url you are going to use as a parameter or what information you are going to send
            return True
    
    def sendData2Web(self, UrlTpye):
        if UrlTpye == "verify":
            values = {'SECRET_KEY': self.secret_key,
                        'code': self.code,
                        'temperature': self.temperature,
                        'facemask': self.face_mask,
                        'mac': self.mac,
                        'sanitizer_perc': self.dispenser_percentage}

            files = {'worker_image': open(self.face_mask_image,'rb')}
            r = requests.post(self.url_verify, files=files, data=values) # * Request WEB
            if r.status_code == 200:
                response_dict = r.json()
                if response_dict["success_message"] == "Allowed":
                    self.allowed = True
                    self.led_color = "Green"
                    pass # TODO: Show Allowed Info
                elif response_dict["error_code"] == 0:
                    self.allowed = False
                    self.led_color = "Red"
                    pass # TODO: Show NOT Allowd Info (Invalid Card)
                elif response_dict["error_code"] == 1:
                    self.allowed = False
                    self.led_color = "Red"
                    pass # TODO: Show NOT Allowd Info (High Temperature) 
                elif response_dict["error_code"] == 2:
                    self.allowed = False
                    self.led_color = "Red"
                    pass # TODO: Show NOT Allowd Info (Not FaceMask Detected)
                self.stage[0] = False
                self.stage[1] = False
                self.stage[2]= False
            else:
                print(r.status_code)
        elif UrlTpye == "init":
            values = {'SECRET_KEY': self.secret_key,
                        'mac': self.mac}
            r = requests.post(self.url_init, data=values) # * Request WEB
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
        if needData:
            dict_response= {'need': needData}
        else:
            dict_response = {'allowed':self.allowed,
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
                                    # ?                 > Pairing Mode
                                    # ?                 > WiFi Settings
                                    # ?                 > Factory Restoration
                                    # ?                 > Need Token (QR page)
        with open('config/info_types_data.json') as json_file:
            self.info_type_data = json.load(json_file)
            json_file.close()
        file_name = self.info_type_data[InfoType].get('file')
        new_content = ""
        with open(f'server/templates/{file_name}', 'r') as file:
            content = file.read()
            for variable in self.info_type_data[InfoType]['variables']:
                content = content.replace(variable , locals()[self.info_type_data[InfoType]['variables'][variable]])
            new_content = content
            file.close()
        with open(f'server/templates/index.html', 'w') as file:
            file.write(new_content)
            file.close()
    



    
