import json
import serial
from pprint import pprint


from data import Data

# * ▼ CONFIG DATA VARIABLES ▼
host = "http://safe.com.ar"
init = "/api/modules/init/"
verify = "/api/modules/verify/"
get_door_status = "/api/modules/get_door_status/"
main_door_update = "/api/modules/main_door_update/"

sk = "qlswpZD6rvyCxkd4jrAkZf2gf5pWI5zn"
# * ▲ CONFIG DATA VARIABLES ▲

# ? TODO: run flask web server here.

if __name__ == "__main__":
    serialPort  = serial.Serial("/dev/ttyS0", baudrate= 9600,) # Used to hold data coming over UART
    #serialString =  '{"code":12345 , "temperature": "None", "dispenser": "None", "joining": 1 }'    
    serialString = ""
    obj_data = Data(host, init, verify, get_door_status, main_door_update, sk)
    obj_data.start()
    print ("Ready...")
    while(1):

        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline().decode('Ascii')
            # Print the contents of the serial data
            
            data_dict = json.loads(serialString)
            print(data_dict)
            if obj_data.analize(data_dict):
                print(obj_data.sendData2Micro())
                # Tell the device connected over the serial port that we recevied the data!
                # The b at the beginning is used to indicate bytes!
                serialPort.write(obj_data.sendData2Micro())
        
            