#!/usr/bin/env python

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

def getTemp():
    return round(weather.temperature(),2)

def getPressure():
    return round(weather.pressure(),2)

def getAcceleration():
    return "\nx: " + str(motion.accelerometer().x)
    + "\ny: " + str(motion.accelerometer().y)
    + "\nz: " + str(motion.accelerometer().z)

def getCurrent1():
    return "\nShunt: " + str(ina219A.getShuntVoltage_mV()) + " mV"
    + "\nBus: " + str(ina219A.getBusVoltage_V()) + " V"
    + "\nCurrent: " + str(ina219A.getCurrent_mA()) + " mA"

def getCurrent2():
    return "\nShunt: " + str(ina219B.getShuntVoltage_mV()) + " mV"
    + "\nBus: " + str(ina219B.getBusVoltage_V()) + " V"
    + "\nCurrent: " + str(ina219B.getCurrent_mA()) + " mA"

def getGPS():
    return "\nLatitude: " + str(gpsd.fix.latitude)
    + "\nLongitude: " + str(gpsd.fix.longitude)

def getAltitude():
    "\nAltitude: " + str(gpsd.fix.altitude)

def getSpeed():
    "\nSpeed: " + str(gpsd.fix.speed)

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
        #Remove output for flight code
        output = """
"Temp: " + str(getTemp()) + "c\n"
"Pressure: " + str(getPressure())+"hPa\n"
"Acceleration: " + str(getAcceleration())
"Current Sensor 0x45: " + str(getCurrent1())
"Current Sensor 0x41: " + str(getCurrent2())
"GPS: " + str(getGPS())
"Altitude: " + str(getAltitude())
"Speed: " + str(getSpeed())


""".format(
    )
        output = output.replace("\n","\n\033[K")
        write(output)
        lines = len(output.split("\n"))
        write("\033[{}A".format(lines - 1))

        time.sleep(1)

except KeyboardInterrupt:
    pass
