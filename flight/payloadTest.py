""" python3-envirophat"" Runs getFrame to collect data from sensors (all except current sensors)
    Sends data to receive module using a transmitting radio module
    Runs when raspberry pi is booted up """

#Import libraries
import sys
import time
#Current sensor library
from Subfact_ina219 import INA219  
#EnviroPhat library (temperature, weather, pressure, acceleration)
from envirophat import weather, motion  
#GPS library
import gps  
from gps import *

import threading
import os
    
from subprocess import call
#GPIO Pin Library
import RPi.GPIO as GPIO

#For xbee
import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600)
string = ""

#serial ports
ser = serial.Serial('/dev/ttyUSB0', 9600)

#roundOff is the number of decimals in the data
roundOff = 4

#Frame is where the data frames are stored
frame = []

""" getFrame is used to gather the following data: time, accelerometer (x,y,z), temperature
    pressure, latitude, longitude, altitude, and speed
    Will have to add current sensor data later when attached to test system """
def getFrame():
    raw_data = { "linux_time" : time.time(),
    "a_x": round(motion.accelerometer().x, roundOff), 
    "a_y": round(motion.accelerometer().y, roundOff),
    "a_z": round(motion.accelerometer().z, roundOff),    
    "t": round(weather.temperature(), roundOff),                        
    "p": round(weather.pressure(), roundOff),                                                
    "lat": round(gpsd.fix.latitude, roundOff),                          
    "lon": round(gpsd.fix.longitude, roundOff),                         
    "alt": round(gpsd.fix.altitude, roundOff),                          
    "sp": round(gpsd.fix.speed, roundOff)}                              

    frame.append(raw_data)

    return raw_data

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
    #start_time = time.time()
    #num = 0
    #while True:
    testFrame = getFrame()
    
    while True:
        getFrame()
        ser.write("Accelerometer")
        ser.write(("x ") + (str)(frame[-1]["a_x"]))
        ser.write(("y ") + (str)(frame[-1]["a_y"]))
        ser.write(("z ") + (str)(frame[-1]["a_z"]))
        ser.write(("Temperature ") + (str)(frame[-1]["t"]))
        ser.write(("Pressure ") + (str)(frame[-1]["p"]))
        ser.write(("Latitude ") + (str)(frame[-1]["lat"]))
        ser.write(("Longitude ") + (str)(frame[-1]["lon"]))
        ser.write(("Altitude ") + (str)(frame[-1]["alt"]))
        ser.write(("Speed ") + (str)(frame[-1]["sp"]))
