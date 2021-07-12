import json
from flask.wrappers import Response
import numpy
import requests
#from getmac import get_mac_address as gma

class Data:
    def __init__(self, url , init , verify , secret_key):

        # * ▼ WEB DATA VARIABLES ▼
        self.url = url
        self.url_init = self.url + init
        self.url_verify = self.url + verify

        self.secret_key = secret_key
        #self.mac = gma()

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
        self.dispenser = bool()
        self.proximity_temp = bool()
        self.proximity_dispenser = bool()


        self.prueba = True

        self.stage = numpy.full(4, False)

        self.info_type_data = dict()

        #self.__dict__.update(dict1)

    def analize(self, dictionary): 

        if dictionary["code"] != "None":
            self.code = dictionary["code"]
            self.joining = dictionary["joining"]
            self.stage[0] = True
            
            pass # TODO: Show Info

        elif dictionary["temperature"] != "None":
            self.temperature = dictionary["temperature"]
            if self.stage[0]:
                self.stage[1] = True
                pass # TODO: Show Info + Temp
            else:
                pass # TODO: Show Only Temp

        elif dictionary["dispenser"] != "None":
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
            pass # TODO: Face Mask Detect
            self.sendData2Web(UrlTpye= False)     # TODO: Determine which url you are going to use as a parameter or what information you are going to send
            return True
    
    def sendData2Web(self, UrlTpye):
        if UrlTpye:
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
                    self.led_color = "Green"
                    self.showInfo("AccessAllowed")
                    pass # TODO: Preparar respuesta
                else:
                    self.allowed = False
                    self.led_color = "Red"
                    pass # TODO: Show NOT Allowd Info
                self.stage[0] = False
                self.stage[1] = False
                self.stage[2]= False
                print(response_dict)
            else:
                print(r.status_code)
            pass # TODO: Http request for the other cases
    
    def sendData2Micro(self):
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
                                    # !                 > Token Change
        with open('data.json') as json_file:
            self.info_type_data = json.load(json_file)
            json_file.close()
        file_name = self.info_type_data[InfoType].get('file')
        new_content = ""
        with open(f'templates/{file_name}', 'r') as file:
            content = file.read()
            for variable in self.info_type_data[InfoType]['variables']:
                content = content.replace(variable , locals()[self.info_type_data[InfoType]['variables'][variable]])
            new_content = content
            file.close()
        with open(f'templates/index.html', 'w') as file:
            file.write(new_content)
            file.close()
        




    
