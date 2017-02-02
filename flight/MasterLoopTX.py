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
txfile = open("testsend.txt", "w")
FRAMESIZE = 39
DECSIZE = 93

#roundOff is the number of decimals in the data
#ROUNDOFF of 2 is confirmed to work
roundOff = 3

#Defines I2C address of current sensors
ina219A = INA219(0x45)
ina219B = INA219(0x41)

#Stores many frames of data
frame = []

def binToAscii(x):
	if(len(x)%8!=0):
		for i in range((8-(len(str(x))%8))):
			x='0'+x
	split = [x[i:i+8] for i in range(0, len(x), 8)]
	asciiStr = ''
	for x in split:
		asciiStr+=chr(int(x, 2))
	return asciiStr

def decToBin(x):
	x = int(x)
	return(((str(bin(x)))[2:]).rstrip("L"))

class DataPoint:
	#name in dictionary
	name = ""
	#head digit for positivity
	hasPositivity = 0
	#amount of digits including the head
	length = 0
	#digits decimal offset count
	decOffset = 0

	def __init__(self, name, hasPositivity, length, decOffset):
		self.name = name
		self.hasPositivity = hasPositivity
		self.length = length
		self.decOffset = decOffset

def frameAssembly(testFrame):
	cAssembly = ""
	cAssembly += str(int(testFrame["time"]*1000))
	cAssembly += str(testFrame["flight_mode"])
	cAssembly += str(testFrame["squib_deployed"])
	cAssembly += str(abs(int(testFrame["temp"]*10))).zfill(4)[-4:]
	cAssembly += str(abs(int(testFrame["pressure"]/10))).zfill(5)[-5:]
	cAssembly += str(abs(int(testFrame["current_1"]*10))).zfill(4)[-4:]
	cAssembly += str(abs(int(testFrame["volt_b1"]*1000))).zfill(4)[-4:]
	cAssembly += str(abs(int(testFrame["current_2"]*10))).zfill(4)[-4:]
	cAssembly += str(abs(int(testFrame["volt_b2"]*1000))).zfill(4)[-4:]
	cAssembly += "0" + str(int(testFrame["gps_lat"]*1000000)).zfill(9)[-9:] if testFrame["gps_lat"] > 0 else "1" + str(abs(int(testFrame["gps_lat"]*1000000))).zfill(9)[-9:]
	cAssembly += "0" + str(int(testFrame["gps_lon"]*1000000)).zfill(9)[-9:] if testFrame["gps_lon"] > 0 else "1" + str(abs(int(testFrame["gps_lon"]*1000000))).zfill(9)[-9:]
	cAssembly += str(abs(int(testFrame["gps_alt"]*10))).zfill(5)[-5:]
	cAssembly += str(abs(int(testFrame["gps_spd"]*10))).zfill(4)[-4:]
	cAssembly += "0" + str(int(testFrame["a_x"]*10)).zfill(3)[-3:] if testFrame["a_x"] > 0 else "1" + str(abs(int(testFrame["a_x"]*10))).zfill(3)[-3:]
	cAssembly += "0" + str(int(testFrame["a_y"]*10)).zfill(3)[-3:] if testFrame["a_y"] > 0 else "1" + str(abs(int(testFrame["a_y"]*10))).zfill(3)[-3:]
	cAssembly += "0" + str(int(testFrame["a_z"]*10)).zfill(3)[-3:] if testFrame["a_z"] > 0 else "1" + str(abs(int(testFrame["a_z"]*10))).zfill(3)[-3:]
	cAssembly += "0" + str(int(testFrame["mag_x"]/10)).zfill(3)[-3:] if testFrame["mag_x"] > 0 else "1" + str(abs(int(testFrame["mag_x"]/10))).zfill(3)[-3:]
	cAssembly += "0" + str(int(testFrame["mag_y"]/10)).zfill(3)[-3:] if testFrame["mag_y"] > 0 else "1" + str(abs(int(testFrame["mag_y"]/10))).zfill(3)[-3:]
	cAssembly += "0" + str(int(testFrame["mag_z"]/10)).zfill(3)[-3:] if testFrame["mag_z"] > 0 else "1" + str(abs(int(testFrame["mag_z"]/10))).zfill(3)[-3:]
	return cAssembly

# testFrame = { 
# 	"time": time.time(),
# 	"flight_mode": 0,
# 	"squib_deployed": 0,
# 	"temp": 24.1167,
# 	"pressure": 100753.5629,
# 	"current_1": -519.0,
# 	"volt_b1": 3.84,
# 	"current_2": -1.0,
# 	"volt_b2": 1.024,
# 	"gps_lat": 37.275995,
# 	"gps_lon": -121.82688,
# 	"gps_alt": 143.3,
# 	"gps_spd": 1.999,
# 	"a_x": 0.0677,
# 	"a_y": -0.0447,
# 	"a_z": 1.0335,
# 	"mag_x": 1395,
# 	"mag_y": -2182,
# 	"mag_z": -3231 }

FRAME_STRUCT = []
FRAME_STRUCT.append(DataPoint("time", 0, 13, 0))
FRAME_STRUCT.append(DataPoint("flight_mode", 0, 1, 0))
FRAME_STRUCT.append(DataPoint("squib_deployed", 0, 1, 0))
FRAME_STRUCT.append(DataPoint("temp", 0, 4, 1))
FRAME_STRUCT.append(DataPoint("pressure", 0, 5, -1))
FRAME_STRUCT.append(DataPoint("current_1", 0, 4, 1))
FRAME_STRUCT.append(DataPoint("volt_b1", 0, 4, 3))
FRAME_STRUCT.append(DataPoint("current_2", 0, 4, 1))
FRAME_STRUCT.append(DataPoint("volt_b2", 0, 4, 3))
FRAME_STRUCT.append(DataPoint("gps_lat", 1, 10, 6))
FRAME_STRUCT.append(DataPoint("gps_lon", 1, 10, 6))
FRAME_STRUCT.append(DataPoint("gps_alt", 0, 5, 1))
FRAME_STRUCT.append(DataPoint("gps_spd", 0, 4, 1))
FRAME_STRUCT.append(DataPoint("a_x", 1, 4, 1))
FRAME_STRUCT.append(DataPoint("a_y", 1, 4, 1))
FRAME_STRUCT.append(DataPoint("a_z", 1, 4, 1))
FRAME_STRUCT.append(DataPoint("mag_x", 1, 4, -1))
FRAME_STRUCT.append(DataPoint("mag_y", 1, 4, -1))
FRAME_STRUCT.append(DataPoint("mag_z", 1, 4, -1))

"""Generates frames of data that contain: raw acceleration values,
magnetometer, gps, and etc. and adds it to the frames array
"""
global flightMode = 0
global squibDeployed = 0
global altArray = []
def getFrame():
	altArray.append(round(weather.altitude(qnh=1020), roundOff))
    raw_data = { "time" : (time.time()),
                 "flight_mode": flightMode,
                 "squib_deployed": squibDeployed,
                 "a_x": round(motion.accelerometer().x, roundOff),
                 "a_y": round(motion.accelerometer().y, roundOff),
                 "a_z": round(motion.accelerometer().z, roundOff),
                 "temp": round(weather.temperature(), roundOff),
                 "pressure": round(weather.pressure(), roundOff),
                 "volt_b1": round(ina219A.getBusVoltage_V(), roundOff),
                 "current_1": round(ina219A.getCurrent_mA(), roundOff),
                 "volt_b2": round(ina219B.getBusVoltage_V(), roundOff),
                 "current_2": round(ina219B.getCurrent_mA(), roundOff),
#"gps_lat": 11,
#"gps_lon": 12,
#"gps_alt": 13,
#"gps_spd": 14,
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
        if ((gpsd.fix.latitude > 0.0) or (gpsd.fix.latitude < 0.0)) and ((gpsd.fix.altitude > 0.0) or (gpsd.fix.altitude < 0.0)):
	    	# print("GPS Locked")
            go = False
        else:
            # print("GPS NOT LOCKED")
            time.sleep(0.5)

#### ---------- Main Loop ---------- ####

def sendFrame():
	try:
		getFrame()
		currentFrame = frame[-1]
		assembledFrame = frameAssembly(currentFrame)
		cFrameBin = decToBin(assembledFrame)
		cFrameEncoded = binToAscii(cFrameBin)
		ser.write(cFrameEncoded)
		txfile.write(cFrameEncoded)
		txfile.write("\n")
		time.sleep(0.05)
	except(KeyboardInterrupt):
        gpsp.running = False
        gpsp.join()
        txfile.close()
        ser.close()

def apogeeCheck():
	#Check for change in pressure and store in pressureChange
	altChange = altArray[-1] - altArray[-2]
	if altChange < 0.0 :
		return 1
	else:
		return 0

global init_altitude = round(gpsd.fix.altitude, roundOff)
def landCheck():
	if abs(round(gpsd.fix.altitude, roundOff) - init_altitude) < 30:
		return 1
	else:
		return 0


global mode = "pre_one"
while mode = "pre_one":
	sendFrame()
	if frame[-1]["current_1"] > 3.0:
		mode = "pre_two"
while mode = "pre_two:
	sendFrame()
	if frame[-1]["voltage_2"] > 9.0:
		flightMode = 1
		mode = "flight"
while mode = "flight":
	sendFrame()
	if apogeeCheck() == 1:
		#trigger squib
		squibDeployed = 1
		flightmode = 2
		mode = "descent"
while mode = "descent":
	sendFrame()
	if landCheck() == 1:
		flightmode = 3
		mode = "recovery"
while True:
	sendFrame()
#### ---------- End of Main Loop ---------- ####
