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

#### ---------- GPS ---------- ####
# GPS init
call(["sudo", "systemctl", "stop", "gpsd.socket"])
call(["sudo", "systemctl", "disable", "gpsd.socket"])
call(["sudo", "killall", "gpsd"])
call(["sudo", "gpsd", "/dev/ttyS0", "-F", "/var/run/gpsd.sock"])
#end GPS init
 
# GPS variables
gpsd = None
 
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

ser = serial.Serial('/dev/ttyUSB0', 9600)
txfile = open("testsend.txt", "w")
FRAMESIZE = 39
DECSIZE = 93
roundOff = 3 #2 is confirmed to work

#Defines I2C address of current sensors
ina219A = INA219(0x45)
ina219B = INA219(0x41)

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

frame = [] #a list of dictionaries that stores frames of data
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
QNH = round(weather.pressure() / 100,2)

#flight variables that will be updated in get frame
global flightMode
flightMode = 0
global squibDeployed
squibDeployed = 0
altArray = []
corrAltArray = []
for i in range(50):
	altArray.append(0)
	corrAltArray.append(0)

#kalman filter variables.  Note that pressure data is already filtered
global k1
k1 = 0.0 #initial value estimation
global k2
k2 = 2.0 #initial error estimation
global k3
k3 = 0.2 #process noise
global k4
k4 = 1.0 #sensor noise
global k5
k5 = 0.0 #initialize a variable used later

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

"""Generates frames of data that contain: raw acceleration values,
magnetometer, gps, and etc. and adds it to the frames array
"""
def getFrame():
	altArray.append(round(weather.altitude(QNH), 1))
	#update filter
	global k1
	global k2
	global k3
	global k4
	global k5
    	k2 += k3
    	k5 = k2/(k2+k4)
    	k1 += (k5*(altArray[-1]-k1))
    	k2 *= (1-k5)
	corrAltArray.append(round(k1, 0))
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
                "gps_lat": round(gpsd.fix.latitude, roundOff),
                "gps_lon": round(gpsd.fix.longitude, roundOff),
                "gps_alt": round(gpsd.fix.altitude, roundOff),
                "gps_spd": round(gpsd.fix.speed, roundOff),
                "mag_x": round(motion.magnetometer().x, roundOff),
                "mag_y": round(motion.magnetometer().y, roundOff),
                "mag_z": round(motion.magnetometer().z, roundOff)}
	frame.append(raw_data)

def sendFrame():
	getFrame()
	currentFrame = frame[-1]
	assembledFrame = frameAssembly(currentFrame)
	cFrameBin = decToBin(assembledFrame)
	cFrameEncoded = binToAscii(cFrameBin)
	ser.write("\x7F\x7F" + cFrameEncoded + "\x00\x00")
	txfile.write(str(currentFrame))
	txfile.write("\n")
	print(str(currentFrame))

def apogeeCheck():
	#Check for change in pressure and store in pressureChange
	if (mode == "flight") and abs(corrAltArray[-1] - corrAltArray[-10] < 5):
		return True
	return False

def landCheck():
	if (mode == "descent" and (abs(corrAltArray[-1] - corrAltArray[-40]) < 1)):
		return True
	return False

#### ---------- Main Loop ---------- ####
if __name__ == '__main__':
    gpsp = GpsPoller()
    gpsp.start()
    while True:
        if ((gpsd.fix.latitude > 0.0) or (gpsd.fix.latitude < 0.0)) and ((gpsd.fix.altitude > 0.0) or (gpsd.fix.altitude < 0.0)):
	    	# print("GPS Locked")
            break
        else:
            # print("GPS NOT LOCKED")
            time.sleep(0.5)
while True:
	try:
		while flightMode == 0:
			sendFrame()
			if frame[-1]["current_1"] > 3.0:
				flightMode = 1
		while flightMode == 1:
			sendFrame()
			if frame[-1]["volt_b2"] > 9.0:
				flightMode = 2
		launchFlag = False
		while flightMode == 2:
			sendFrame()
			if abs(frame[-1]["a_z"] < 1.5):
				launchFlag = True
			if launchFlag and apogeeCheck():
				#trigger squib
				squibDeployed = 1
				flightMode = 3
				mode = "descent"
		while flightMode == 3:
			if landCheck():
				flightmode = 4
	except(KeyboardInterrupt):
		gpsp.running = False
		gpsp.join()
		txfile.close()
		ser.close():

	#### ---------- End of Main Loop ---------- ####
