#!/usr/bin/env python

import sys
ximport time
from Subfact_ina219 import INA219
from envirophat import weather, motion
import gps
from gps import *
import threading
import os
from subprocess import call
import RPi.GPIO as GPIO

def getTemp():
    return round(weather.temperature(),2)

def getPressure():
    return round(weather.pressure(),2)

def getAcceleration():
    return "\nx: " + str(motion.accelerometer().x) + "\ny: " + str(motion.accelerometer().y) + "\nz: " + str(motion.accelerometer().z)

def getCurrent1():
    return "\nShunt: " + str(ina219A.getShuntVoltage_mV()) + " mV" + "\nBus: " + str(ina219A.getBusVoltage_V()) + " V" + "\nCurrent: " + str(ina219A.getCurrent_mA()) + " mA"

def getCurrent2():
    return "\nShunt: " + str(ina219B.getShuntVoltage_mV()) + " mV" + "\nBus: " + str(ina219B.getBusVoltage_V()) + " V" + "\nCurrent: " + str(ina219B.getCurrent_mA()) + " mA"

def getGPS():
    return "\nLatitude: " + str(gpsd.fix.latitude) + "\nLongitude: " + str(gpsd.fix.longitude) + "\nAltitude: " + str(gpsd.fix.altitude) + "\nSpeed: " + str(gpsd.fix.speed)+ "\nTime: " + str(gpsd.fix.time)

ina219A = INA219(0x45)
ina219B = INA219(0x41)

resultA = ina219A.getBusVoltage_V()
resultB = ina219B.getBusVoltage_V()

#### ---------- GPS ---------- ####

# GPS variables
gpsd = None

# GPS init
call(["sudo", "systemctl", "stop", "gpsd.socket"])
call(["sudo", "systemctl", "disable", "gpsd.socket"])
call(["sudo", "gpsd", "/dev/ttyS0", "-F", "/var/run/gpsd.sock"])

class GpsPoller(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                global gpsd #bring it in scope
                gpsd = gps(mode = WATCH_ENABLE) #starting the stream of info
                self.current_value = None
                self.running = True #setting the thread running to true
        def run(self):
                global gpsd
                while gpsp.running:
                        gpsd.next()

if __name__ == '__main__':
    gpsp = GpsPoller()
    gpsp.start()
    # Waits for GPS to get a Fix
    time.sleep(30)

def write(line):
    sys.stdout.write(line)
    sys.stdout.flush()

write("--- Enviro pHAT Monitoring ---")

try:
    while True:
	print ("Temp: " + str(getTemp()) + "c\n")
	print ("Pressure: " + str(getPressure())+"hPa\n")
	print ("Acceleration: " + str(getAcceleration()))
	print ("Current Sensor 0x45: " + str(getCurrent1()))
	print ("Current Sensor 0x41: " + str(getCurrent2()))
	print ("GPS: " + str(getGPS()))

        time.sleep(1)

except KeyboardInterrupt:
    pass
