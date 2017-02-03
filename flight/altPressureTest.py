import sys
import time
from Subfact_ina219 import INA219
from envirophat import weather, motion
import gps
from gps import *
import threading
import os
from subprocess import call
import RPi.GPIO as GPIO

#Assuming altitude is measured in meteres
x = 100.0 #initial value 
p = 2.0 #estimated error 
q = 0.2 #process noise
r = 1.0 #sensor noise
frames = [] #corrected value
errors = [] #measured value
roundOff = 0

def getFrame():
    raw_data = { "linux_time": (time.time()),
                 "alt_pres": round(weather.altitude(qnh=1020), roundOff)
                 }
    errors.append(raw_data)    

getFrame()
while True:
    getFrame()
    
    #update filter
    p += q
    k = p/(p+r)
    x += (k*(errors[-1]["alt_pres"]-x))
    p *= (1-k)

    #display and update data
    frames.append(x)
    print(errors[-1]["alt_pres"], round(frames[-1], roundOff))
    time.sleep(0.05)

