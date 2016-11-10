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

#serial port
ser = serial.Serial('/dev/ttyUSB0', 9600)

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
    raw_data = { "linux_time" : time.time(),
    "a_x": round(motion.accelerometer().x, roundOff), 
    "a_y": round(motion.accelerometer().y, roundOff),
    "a_z": round(motion.accelerometer().z, roundOff),    
    "t": round(weather.temperature(), roundOff),                        
    "p": round(weather.pressure(), roundOff),                           
    "s1": round(ina219A.getShuntVoltage_mV(), roundOff),                
    "b1": round(ina219A.getBusVoltage_V(), roundOff),                  
    "c1": round(ina219A.getCurrent_mA(), roundOff),                     
    "s2": round(ina219B.getShuntVoltage_mV(), roundOff),                
    "b2": round(ina219B.getBusVoltage_V(), roundOff),                   
    "c2": round(ina219B.getCurrent_mA(), roundOff),                     
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
    num = 0
    while True:
        getFrame()
	print (("time ") + (str)(frame[num]["linux_time"]))
    	print (("x ") + (str)(frame[num]["a_x"]))
	print (("y ") + (str)(frame[num]["a_y"]))
	print (("z ") + (str)(frame[num]["a_z"]))
	print ("")
   	num = num + 1
    
    #total_time = str(time.time() - start_time)
   
    #print("Time to run: " + total_time)
    #time.sleep(5)
