import network, urequests, ujson

WIFI_SSID = 'ssid'
WIFI_PASSWORD = 'password'
DOOR_MAC = 1
ENV_UPDATE_URL = 'http://...:8000/api/modules/env_update/'
SECRET_KEY = 'secretkey'

def connect_to_wifi():
    
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        print('Connecting to network ' + WIFI_SSID + ' ...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
        print('Connected!')

def env_update(co2_level, co_level, metano_level, lpg_level):
    try:

        data = {
                'SECRET_KEY': SECRET_KEY,
                'door_mac': DOOR_MAC,
                'co2_level': co2_level,
                'co_level': co_level,
                'metano_level': metano_level,
                'lpg_level': lpg_level,
            }
        
        print('Sending request')
        
        response = urequests.post(ENV_UPDATE_URL, json = data, headers = {'content-type': 'application/json'}).json()

        #print(response)

    except Exception as e:
        print('Error: ' + str(e))
