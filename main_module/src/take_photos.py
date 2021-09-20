# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import os

FILE_DIR = os.path.dirname(__file__) + "/"
# initialize the camera and grab a reference to the raw camera capture
def takePhotos(times):
    camera = PiCamera()
    rawCapture = PiRGBArray(camera)
    # allow the camera to warmup
    time.sleep(0.1)
    # grab an image from the camera
    count = 0
    while count < times:
        # display the image on screen and wait for a keypress
        count = count + 1
        name = f"images/input/picture_{count}.jpg"
        print(name)
        camera.capture(name)
        cv2.waitKey(10)