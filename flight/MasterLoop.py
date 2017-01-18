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


ser = serial.Serial('/dev/ttyUSB0', 9600)
startfile = open("teststart.txt", "w")

#roundOff is the number of decimals in the data
roundOff = 2

#Defines I2C address of current sensors
ina219A = INA219(0x45)
ina219B = INA219(0x41)

#Stores many frames of data
frame = []
gpsd = None

"""Generates frames of data that contain: raw acceleration values,
magnetometer, gps, and etc. and adds it to the frames array
"""
def binToAscii(x):
	if(len(x)%8!=0):
		for i in range((8-(len(str(x))%8))):
			x='0'+x
	split = [x[i:i+8] for i in range(0, len(x), 8)]
	asciiStr = ''
	for x in split:
		asciiStr+=chr(int(x, 2))
	return asciiStr

def asciiToBin(x):
	binStr = ''
	for i in x:
		binStr+=str(((bin(ord(i)))[2:]).zfill(8))
	return binStr

def decToBin(x):
	x = int(x)
	return(((str(bin(x)))[2:]).rstrip("L"))

def binToDec(x):
	return(str(int(str(x),2)))

def frameAssembly(testFrame):
    cFrame = ""
    cFrame += str(int(testFrame["time"]*1000))
    cFrame += str(testFrame["flight_mode"])
    cFrame += str(testFrame["squib_deployed"])
    cFrame += str(abs(int(testFrame["temp"]*10))+1000).zfill(4)[-4:]
    cFrame += str(abs(int(testFrame["pressure"]/10))).zfill(5)[-5:]
    cFrame += str(abs(int(testFrame["current_1"]*10))).zfill(4)[-4:]
    cFrame += str(abs(int(testFrame["volt_b1"]*1000))).zfill(4)[-4:]
    cFrame += str(abs(int(testFrame["current_2"]*10))).zfill(4)[-4:]
    cFrame += str(abs(int(testFrame["volt_b2"]*1000))).zfill(4)[-4:]
    cFrame += "0" + str(int(testFrame["gps_lat"]*1000000)).zfill(9)[-9:] if testFrame["gps_lat"] > 0 else "1" + str(abs(int(testFrame["gps_lat"]*1000000))).zfill(9)[-9:]
    cFrame += "0" + str(int(testFrame["gps_lon"]*1000000)).zfill(9)[-9:] if testFrame["gps_lon"] > 0 else "1" + str(abs(int(testFrame["gps_lon"]*1000000))).zfill(9)[-9:]
    cFrame += str(abs(int(testFrame["gps_spd"]*10))).zfill(4)[-4:]
    cFrame += "0" + str(int(testFrame["a_x"]*10)).zfill(3)[-3:] if testFrame["a_x"] > 0 else "1" + str(abs(int(testFrame["a_x"]*10))).zfill(3)[-3:]
    cFrame += "0" + str(int(testFrame["a_y"]*10)).zfill(3)[-3:] if testFrame["a_y"] > 0 else "1" + str(abs(int(testFrame["a_y"]*10))).zfill(3)[-3:]
    cFrame += "0" + str(int(testFrame["a_z"]*10)).zfill(3)[-3:] if testFrame["a_z"] > 0 else "1" + str(abs(int(testFrame["a_z"]*10))).zfill(3)[-3:]
    cFrame += "0" + str(int(testFrame["mag_x"]/10)).zfill(3)[-3:] if testFrame["mag_x"] > 0 else "1" + str(abs(int(testFrame["mag_x"]/10))).zfill(3)[-3:]
    cFrame += "0" + str(int(testFrame["mag_y"]/10)).zfill(3)[-3:] if testFrame["mag_y"] > 0 else "1" + str(abs(int(testFrame["mag_y"]/10))).zfill(3)[-3:]
    cFrame += "0" + str(int(testFrame["mag_z"]/10)).zfill(3)[-3:] if testFrame["mag_z"] > 0 else "1" + str(abs(int(testFrame["mag_z"]/10))).zfill(3)[-3:]
    return cFrame

def getFrame():
    raw_data = { "time" : (time.time()),
                 "flight_mode": 0,
                 "squib_deployed": 0,
    "a_x": round(motion.accelerometer().x, roundOff), 
    "a_y": round(motion.accelerometer().y, roundOff),
    "a_z": round(motion.accelerometer().z, roundOff),    
    "temp": round(weather.temperature(), roundOff),                        
    "pressure": round(weather.pressure(), roundOff),                                         
    "volt_b1": round(ina219A.getBusVoltage_V(), roundOff),                  
    "current_1": round(ina219A.getCurrent_mA(), roundOff),                                    
    "volt_b2": round(ina219B.getBusVoltage_V(), roundOff),                   
    "current_2": round(ina219B.getCurrent_mA(), roundOff),
                 #"gps_lat": 12, "gps_lon": 13, "gps_alt":14, "gps_spd":15,
    "gps_lat": round(gpsd.fix.latitude, roundOff),                          
    "gps_lon": round(gpsd.fix.longitude, roundOff),                         
    "gps_alt": round(gpsd.fix.altitude, roundOff),                          
    "gps_spd": round(gpsd.fix.speed, roundOff),
                 "mag_x": round(motion.magnetometer().x, roundOff),
                 "mag_y": round(motion.magnetometer().y, roundOff),
                 "mag_z": round(motion.magnetometer().z, roundOff)
                 }                              
    frame.append(raw_data)



 
#### ---------- GPS ---------- ####
 
# GPS variables
gpsd = None
 
# GPS init
call(["sudo", "systemctl", "stop", "gpsd.socket"])
call(["sudo", "systemctl", "disable", "gpsd.socket"])
call(["sudo", "gpsd", "/dev/ttyUSB0", "-F", "/var/run/gpsd.sock"])
 
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
    go = True
    while go:
        if gpsd.fix.latitude != 0.0:
            go = False
            print("GPS Locked")
        else:
            time.sleep(0.5)

num = 0
while True:
    try:
        getFrame()
        currFrame = frame[num]
        cFrame = frameAssembly(currFrame)
        cFrameBin = decToBin(cFrame)
        cFrameEncoded = binToAscii(cFrameBin)
        ser.write(cFrameEncoded)
        startfile.write(cFrameEncoded)
        startfile.write("\n")
        num += 1
        time.sleep(0.02)
    except (KeyboardInterrupt):
        gpsp.running = False
        gpsp.join()
        startfile.close()
        ser.close()  	
        break    

