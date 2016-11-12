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

def getFrame():
    raw_data = { "linux_time": (time.time()),
                 "a_x": round(motion.accelerometer().x, roundOff),
                 "a_y": round(motion.accelerometer().y, roundOff)
                 }
    frame.append(raw_data)

def velocityX():
    return (((frame[-1]["a_x"])+(frame[-2]["a_x"]) * .5) * ((frame[-1]["linux_time"]) - (frame[-2]["linux_time"])) + v_xi)    

def velocityY():
    return (((frame[-1]["a_y"])+(frame[-2]["a_y"]) * .5) * ((frame[-1]["linux_time"]) - (frame[-2]["linux_time"])) + v_yi)

i = 0
v_xi = 0
v_yi = 0

while True:
    getFrame()
    print (frame[-1]["a_x"])
    print (frame[-1]["a_y"])
    #if (abs(frame[-1]["a_x"])  > 0.1 and abs(frame[-1]["a_y"]) > 0.1):
    getFrame()
    print(round(velocityX(), roundOff))
    print(round(velocityY(), roundOff))
    v_xi = velocityX() 
    v_yi = velocityY()
    print
    getFrame()
    i = i + 1
    if i == 2:
        getFrame()
        p_x = (round(((velocityX() + v_xi) * 0.5) * ((frame[-1]["linux_time"]) - (frame[-4]["linux_time"]))), roundOff)
        p_y = (round(((velocityY() + v_yi) * 0.5) * ((frame[-1]["linux_time"]) - (frame[-4]["linux_time"]))), roundOff)
        print(p_x)
        print(p_y)
        print()
        i = 0
    
    
