"""
import os
os.system("raspistill -o foto_%04d.jpg -tl 30000 -t 1000")
"""

"""
from time import sleep
from picamera import PiCamera

camera = PiCamera(resolution=(1280, 720), framerate=30)
# Set ISO to the desired value
camera.iso = 100
camera.capture_sequence(['imagenAAAA%02d.jpg' % i for i in range(99) ]sleep(5))
# Wait for the automatic gain control to settle
"""
"""
for i in range(99):    
    sleep(5)
    # Now fix the values
    #camera.shutter_speed = 1000000
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_gains = g
    # Finally, take several photos with the fixed settings
    #camera.capture_sequence(['imagen%02d.jpg' % i for i in range(99)])
    #camera.capture_sequence('imagenA%02d.jpg', str(i))
"""
"""

import time
import picamera

with picamera.PiCamera() as picam:
    picam.start_preview()
    picam.brightness= 50
    picam.ISO =100 
    time.sleep(3) 
    picam.shutter_speed= 900000
    picam.capture('foto3.1.jpg') 
    picam.stop_preview() 
"""

"""
import time
import picamera

with picamera.PiCamera() as picam:
    picam.start_preview()
    picam.start_recording('video.h264')
    picam.wait_recording(10)
    picam.stop_recording(10)
    picam.stop_preview()
    picam.close()

"""
"""
import os
os.system("raspistill -o nombre7.png")
"""
import os
os.system("raspistill -o ej2-%04d.jpg -w 1280 -h 720 -tl 10000 -t 200000")