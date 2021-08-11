import network

def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect('Paletta_WiFi', 'tele-2979543')
        while not sta_if.isconnected():
            pass
        
    print('Network config:', sta_if.ifconfig())
    
do_connect()