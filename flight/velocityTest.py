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

def velocityX(i):
    return (((((frame[i]["a_x"])+(frame[i-1]["a_x"])) * .5) * ((frame[i]["linux_time"]) - (frame[i-1]["linux_time"]))) + v_xi)    
    

def velocityY():
    return (((((frame[-1]["a_y"])+(frame[-2]["a_y"])) * .5) * ((frame[-1]["linux_time"]) - (frame[-2]["linux_time"]))) + v_yi)

i = 1
v_xi = 0
v_yi = 0
getFrame()
while True:
    getFrame()
    vinstx=velocityX(i)
    #print (frame[-1]["a_x"])
    #print (frame[-1]["a_y"])
    #if (abs(frame[-1]["a_x"])  > 0.1 and abs(frame[-1]["a_y"]) > 0.1):
    print(round(vinstx, roundOff))
    print ("\n")
    #print(round(velocityY(), roundOff))
    v_xi = vinstx 
    v_yi = velocityY()
    i = i + 1
    #if i == 2:
        #getFrame()
        #p_x = (round(((velocityX() + v_xi) * 0.5) * ((frame[-1]["linux_time"]) - (frame[-4]["linux_time"]))), roundOff)
        #p_y = (round(((velocityY() + v_yi) * 0.5) * ((frame[-1]["linux_time"]) - (frame[-4]["linux_time"]))), roundOff)
        #print(p_x)
        #print(p_y)
        #print
        #i = 0
    
    
