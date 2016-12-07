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

frame = []
roundOff = 1
dropout = 0.1

def getFrame():
    raw_data = { "linux_time": (time.time()),
                 "a_x": round(motion.accelerometer().x, roundOff),
                 "a_y": round(motion.accelerometer().y, roundOff)
                 }
    frame.append(raw_data)

def velocityX(): #calculates area from t-1 to t
    af = round(frame[-1]["a_x"], roundOff)
    ai = round(frame[-2]["a_x"], roundOff)
    vs = 0.0
    if abs(af) > dropout:
        dt = frame[-1]["linux_time"] - frame[-2]["linux_time"]
        vs = ((af + ai) * .5 * dt)
    return vs
# Main

getFrame()
vsum = 0
while True:
    getFrame()
    vinit = velocityX()
    vsum = vsum + vinit
    print (frame[-1]["a_x"])
    print (vinit)
    print (vsum)
    print
    time.sleep(0.02)
    

