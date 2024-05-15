from picamera2 import Picamera2, Preview
from time import sleep

def ta_bilde():
    camera = Picamera2()
    
    print("åpner kamera")
    camera.start()
    sleep(1)
    camera.capture_file("bilde.jpg")
    print("bilde tatt")
    camera.stop()
    camera.close()
    print("kamera lukket")
