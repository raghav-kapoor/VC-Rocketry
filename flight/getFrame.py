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

#roundOff is the number of decimals in the data
roundOff = 4

#Defines I2C address of current sensors
ina219A = INA219(0x45)
ina219B = INA219(0x41)

#Stores many frames of data
frame = []
num = 0  #num is a test value

"""Generates frames of data that contain: raw acceleration values,
magnetometer, gps, and etc. and adds it to the frames array
"""

def getFrame():
    raw_data = {"a_x": round(motion.accelerometer().x), roundOff),    #x-axis acceleration
    "a_y": round(motion.accelerometer().y, roundOff),                   #y-axis acceleration
    "a_z": round(motion.accelerometer().z, roundOff),                   #z-axis acceleration    
    "t": round(weather.temperature(), roundOff),                        #Temperature
    "p": round(weather.pressure(), roundOff),                           #Pressure
    "s1": round(ina219A.getShuntVoltage_mV(), roundOff),                #Shunt 1 Voltage
    "b1": round(ina219A.getBusVoltage_V(), roundOff),                   #Bus 1 Voltage
    "c1": round(ina219A.getCurrent_mA(), roundOff),                     #Current 1
    "s2": round(ina219B.getShuntVoltage_mV(), roundOff),                #Shunt 2 Voltage
    "b2": round(ina219B.getBusVoltage_V(), roundOff),                   #Bus 2 Voltage
    "c2": round(ina219B.getCurrent_mA(), roundOff),                     #Current 2
    "lat": round(gpsd.fix.latitude, roundOff),                          #Latitude
    "lon": round(gpsd.fix.longitude, roundOff),                         #Longitude
    "alt": round(gpsd.fix.altitude, roundOff),                          #Altitude
    "sp": round(gpsd.fix.speed, roundOff)}                              #Speed

    #Converts time stamp to variable name and assigns it the dictionary values
    linux_time = str((round(time.time(), roundOff)))

    frame.append((var()[linux_time] = raw_data))

start_time = time.time()    
while (num < 1000):
    getFrame()
    num++
print("Time to run: " + (time.time() - start_time))

