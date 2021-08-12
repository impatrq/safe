import network

WIFI_SSID = 'Paletta_WiFi'
WIFI_PASSWORD = 'tele-2979543'
DOOR_MAC = 1

def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        print('Connecting to network ' + WIFI_SSID + ' ...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
        print('Connected!')

