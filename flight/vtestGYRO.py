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
import serial

outfile = file("data.txt", "w")

x = 0.0 #initial value u a2=0
p = 2.0 #estimated error u a2=3
q = 0.1 #process noise i a2=.07
r = 0.5 #sensor noise i a2=3
frames = [0] #corrected value
errors = [] #measured value
vframes = [0]
verrors = [0]

def getFrame():
    raw_data = { "linux_time": (time.time()),
                 "a_x": round(motion.accelerometer().z, 2),
                 #"a_y": round(motion.accelerometer().y, roundOff)
                 }
    errors.append(raw_data)
    
def velocity(a1, a2, tstep): #from t-1 to t
    v = (a1+a2) * 0.5 * tstep * 9.8
    return v
    

getFrame()
vframe = 0
verror = 0
i = 0
while True:
    getFrame()
        
    #update filter
    p += q
    k = p/(p+r)
    x += (k*(errors[-1]["a_x"]-x))
    p *= (1-k)    

    #display and update data
    frames.append(x)
    #velocity stuff
    vframe += velocity(frames[-2], frames[-1], errors[-1]["linux_time"] - errors[-2]["linux_time"])
    verror += velocity(errors[-2]["a_x"], errors[-1]["a_x"], errors[-1]["linux_time"] - errors[-2]["linux_time"])
    vframes.append(vframe)
    verrors.append(verror)
    #if (i%10 == 0):
    #print(round(errors[-1]["a_x"], 1), round(x, 1))
    #print(round(verror, 4), round(vframe, 4))
    print(round(x,2), round(vframe,1))
    time.sleep(0.02)
    outfile.write(str(frames))
    i+=1

