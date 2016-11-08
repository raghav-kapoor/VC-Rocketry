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

"""Generates frames of data that contain: raw acceleration values,
magnetometer, gps, add on later
"""
while True:
    print getFrame()

def getFrame():
    time_stamp = {"a_x": round(motion.accelerometer().x), roundOff),    #x-axis acceleration
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

    linux_time = str((round(time.time(), 4)))
    exec("%s" = time_stamp % (linux_time))
    
    
    
