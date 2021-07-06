# MicroPython ESP32


## Install MicroPython on ESP32:

[Complete Tutorial](https://learn.sparkfun.com/tutorials/how-to-load-micropython-on-a-microcontroller-board/esp32-thing)

- ```ls -l /dev/ttyUSB0```
- [Download MicroPython](https://micropython.org/download/esp32/) 
- ```pip install --upgrade esptool```
- ```esptool.py --chip esp32 -p /dev/ttyUSB0 erase_flash```
- ```esptool.py --chip esp32 -p /dev/ttyUSB0 write_flash -z 0x1000 <path to .bin>```

## Load MicroPython Program to ESP32:

[Complete Tutorial](https://learn.sparkfun.com/tutorials/micropython-programming-tutorial-getting-started-with-the-esp32-thing/all#:~:text=To%20upload%20the%20program%20to,boot.py%20will%20be%20run.)

- ```pip install adafruit-ampy```
- Connect to ```/dev/ttyUSB0``` via serial to test the connection with these following parameters:
    - Speed: 115200 bits per second
    - Data Bits: 8
    - Parity: None
    - Stop Bits: 1
- ```ampy --port /dev/ttyUSB0 put main.py```
