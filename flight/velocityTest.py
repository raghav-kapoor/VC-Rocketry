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
roundOff = 4

def getFrame():
    raw_data = { "linux_time": (time.time()),
                 "a_x": round(motion.accelerometer().x, roundOff),
                 "a_y": round(motion.accelerometer().y, roundOff),
                 }
    frame.append(raw_data)

getFrame()
while True:
    getFrame()
    v_x = (((frame[-1]["a_x"])+(frame[0]["a_x"])) * .5) * (((frame[0]["linux_time"])) - ((frame[-1]["linux_time"])))
    print(v_x)
