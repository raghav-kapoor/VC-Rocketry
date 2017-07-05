import sys
import time
from Subfact_ina219 import INA219
try:
	from envirophat import weather, motion
except:
	print("\nENVIROPHAT NOT CONNECTED\n")
	sys.exit(4) #4 means envirophat not connected
import gps
from gps import *
import threading
import os
import io
from subprocess import call
import RPi.GPIO as GPIO
import serial

#### ---------- GPS ---------- ####
# GPS TERMINAL CLEARS
call(["sudo", "systemctl", "stop", "serial-getty@ttyAMA0.service"])
call(["sudo", "systemctl", "disable", "serial-getty@ttyAMA0.service"])
call(["sudo", "killall", "gpsd"])
call(["sudo", "gpsd", "/dev/ttyAMA0", "-F", "/var/run/gpsd.sock"])

# GPS variables
gpsd = None

#GPS THREADING
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

#DATAPOINT CLASS FOR FRAME
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
	try:
		altArray.append(round(weather.altitude(QNH), 1))
	except:
		altArray.append(0)
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
	raw_data = {"time" : time.time(), "flight_mode": flightMode, "squib_deployed": squibDeployed, "QNH": QNH}
	try:
		raw_data["a_x"] = round(motion.accelerometer().x, roundOff)
	except:
		raw_data["a_x"] = 0.0
	try:
		raw_data["a_y"] = round(motion.accelerometer().y, roundOff)
	except:
		raw_data["a_y"] = 0.0
	try:
		raw_data["a_z"] = round(motion.accelerometer().z, roundOff)
	except:
		raw_data["a_z"] = 0.0
	try:
		raw_data["temp"] = round(weather.temperature(), roundOff)
	except:
		raw_data["temp"] = 0.0
	try:
		raw_data["pressure"] = round(weather.pressure(), roundOff)
	except:
		raw_data["pressure"] = 0.0
	try:
		raw_data["volt_b1"] = round(ina219A.getBusVoltage_V(), roundOff)
	except:
		raw_data["volt_b1"] = 0.0
	try:
		raw_data["current_1"] = round(ina219A.getCurrent_mA(), roundOff)
	except:
		raw_data["current_1"] = 0.0
	try:
		raw_data["volt_b2"] = round(ina219B.getBusVoltage_V(), roundOff)
	except:
		raw_data["volt_b2"] = 0.0
	try:
		raw_data["current_2"] = round(ina219B.getCurrent_mA(), roundOff)
	except:
		raw_data["current_2"] = 0.0
	try:
		raw_data["gps_lat"] = round(gpsd.fix.latitude, roundOff)
	except:
		raw_data["gps_lat"] = 0
	try:
		raw_data["gps_lon"] = round(gpsd.fix.longitude, roundOff)
	except:
		raw_data["gps_lon"] = 0
	try:
		raw_data["gps_alt"] = round(gpsd.fix.altitude, roundOff)
	except:
		raw_data["gps_alt"] = 0
	try:
		raw_data["gps_spd"] = round(gpsd.fix.speed, roundOff)
	except:
		raw_data["gps_spd"] = 0
	try:
		raw_data["mag_x"] = round(motion.magnetometer().x, roundOff)
	except:
		raw_data["mag_x"] = 0.0
	try:
		raw_data["mag_y"] = round(motion.magnetometer().y, roundOff)
	except:
		raw_data["mag_y"] = 0.0
	try:
		raw_data["mag_z"] = round(motion.magnetometer().z, roundOff)
	except:
		raw_data["mag_z"] = 0.0
	raw_data["altP"] = corrAltArray[-1]
	for key in raw_data.keys():
		if (type(raw_data[key]) is not float) and (type(raw_data[key]) is not int):
			raw_data[key] = 0
		if (raw_data[key] != raw_data[key]):
			raw_data[key] = 0
        frame.append(raw_data)

def sendFrame():
	getFrame()
	currentFrame = frame[-1]
	assembledFrame = frameAssembly(currentFrame)
	cFrameBin = decToBin(assembledFrame)
	cFrameEncoded = binToAscii(cFrameBin)
	try:
		ser.write("\x7F\x7F" + cFrameEncoded + "\x00\x00")
	except:
		print("\nRADIO MODULE ERROR\n")
		txfile.write("\nRADIO MODULE ERROR\n")
	txfile.write(str(currentFrame))
	txfile.write("\n")
	print(str(currentFrame))
	time.sleep(0.04)

def apogeeCheck():
        if len(frame) > 10:
                for i in range(10):
                        if frame[-1*i]["altP"] <= 0:
                                return False
                if (flightMode == 3) and abs(frame[-1]["altP"] - frame[-10]["altP"] < 5):
                        return True
	return False

def landCheck():
        if len(frame) > 40:
                if (flightMode == 4) and (abs(frame[-1]["altP"] - frame[-40]["altP"]) < 1):
                        return True
	return False

def flightOperation(mode):
	global flightMode
	global squibDeployed
	global delayStart
	global SQUIBDELAY
	global ground
	global apogeeReached
	if mode == 0:
		if frame[-1]["current_2"] > 300.0:
			flightMode = 1
			configWrite("flightMode", flightMode)
		return
	if mode == 1:
		if frame[-1]["current_2"] < 300.0:
			flightMode = 0
			configWrite("flightMode", flightMode)
			return
		if frame[-1]["volt_b1"] > 8.0:
			flightMode = 2
			configWrite("flightMode", flightMode)
		return
	if mode == 2:
		if frame[-1]["current_2"] < 300.0 or frame[-1]["volt_b1"] < 8.0:
			flightMode = 0
			configWrite("flightMode", flightMode)
			return
		if abs(frame[-1]["a_z"]) > 3.5:
			flightMode = 3
			ground = 0
			configWrite("flightMode", flightMode)
			configWrite("ground", ground)
		return
	if mode == 3:
		if apogeeCheck():
			apogeeReached = 1
			flightMode = 4
			delayStart = time.time()
			configWrite("flightMode", flightMode)
			configWrite("apogeeReached", apogeeReached)
			configWrite("delayStart", delayStart)
		return
	if mode == 4:
		if frame[-1]["time"] - delayStart > SQUIBDELAY:
			flightMode = 5
			squibDeployed = 1
			configWrite("flightMode", flightMode)
			configWrite("squibDeployed", squibDeployed)
			#trigger pyros
			GPIO.output(20, 1)
			GPIO.cleanup()
		return
	if mode == 5:
		if landCheck():
			flightMode = 6
			ground = 1
			configWrite("flightMode", flightMode)
			configWrite("ground", ground)
		return
	if mode == 6:
		return
	return

def whereAmI():
	global ground
	global squibDeployed
	global apogeeReached
	if ground == 1 and frame[-1]["current_2"] < 3.0:
		return 0
	if ground == 1 and frame[-1]["volt_b1"] < 8.0 and squibDeployed == 0:
		return 1
	if ground == 1 and apogeeReached == 0:
		return 2
	if ground == 0 and apogeeReached == 0:
		return 3
	if ground == 0 and apogeeReached == 1 and squibDeployed == 0:
		return 4
	if ground == 0 and apogeeReached == 1 and squibDeployed == 1:
		return 5
	if ground == 1 and apogeeReached == 1 and squibDeployed == 1:
		return 6
	return 0

# use this function to read a value from the config file 
# pass which parameter you want to read
def configRead(parameter):

        # read a list of lines into data
        with open(path, 'r') as file:
                lines = file.readlines()
		for i in range(len(lines)):
			lines[i] = lines[i].strip()
		
        if parameter == "ground":
                value =  lines[12]

        elif  parameter == "apogeeReached":
                value = lines[15]

        elif parameter == "flightMode":
                value =  lines[18]

        elif parameter == "SQUIBDELAY":
                value = lines[21]

        elif parameter == "delayStart":
                value = lines[24]

        elif parameter == "QNH":
                value = lines[27]

        elif parameter == "FRAMESIZE":
                value = lines[30]

        elif parameter == "DECSIZE":
                value = lines[33]

        elif parameter == "roundOff":
                value = lines[36]

        elif parameter == "k1":
                value = lines[39]

        elif parameter == "k2":
                value = lines[42]

        elif parameter == "k3":
                value = lines[45]

        elif parameter == "k4":
                value = lines[48]

        elif parameter == "k5":
                value = lines[51]

        elif parameter == "passedCutoff":
                value = lines[54]

        elif parameter == "squibDeployed":
                value = lines[57]
	
	elif parameter == "cutoff":
		value = lines[60]
	
        return value.strip()

# use this function to write a value to the config file 
# pass which parameter you want to change and the new value
def configWrite(parameter, val):
	

        value = str(val)
        value += " \n" 

	# read a list of lines into data
	with open(path, 'r') as file:
                lines = file.readlines()

	# change desired value

	if parameter == "ground":
		lines[12] = value

	elif parameter == "apogeeReached":
		lines[15] = value

	elif parameter == "flightMode":
		lines[18] = value

	elif parameter == "SQUIBDELAY":
		lines[21] = value

	elif parameter == "delayStart":
		lines[24] = value

	elif parameter == "QNH":
		lines[27] = value

	elif parameter == "FRAMESIZE":
		lines[30] = value

	elif parameter == "DECSIZE":
		lines[33] = value

	elif parameter == "roundOff":
		lines[36] = value

	elif parameter == "k1":
		lines[39] = value

	elif parameter == "k2":
		lines[42] = value

	elif parameter == "k3":
		lines[45] = value

	elif parameter == "k4":
		lines[48] = value

	elif parameter == "k5":
		lines[51] = value

	elif parameter == "passedCutoff":
		lines[54] = value

	elif parameter == "squibDeployed":
                lines[57] = value
	
	elif parameter == "cutoff":
		lines[60] = value

	# and write everything back
	with open(path, 'w') as file:
		file.writelines(lines)
	
#### ---------- Main Loop ---------- ####			
###NEW MAIN CONTROL FUNCTIONALITY

#Open a file to write to
txfile = open("/home/pi/VC-Rocketry/flight/" + str(time.time()) + ".txt", "w")

#GPS STARTUP
try:
	gpsp = GpsPoller()
	gpsp.start()
except:
	print("\nGPS NOT FUNCTIONAL\n")
	txfile.write("\nERROR 3: GPS NOT FUNCTIONAL\n")
	txfile.close()
	sys.exit(3) #3 for GPS errors

###END GPS INITIALIZATION

#OPEN SERIAL COMMUNICATION PORT
try:
	ser = serial.Serial('/dev/ttyUSB0', 9600)
except:
	print("\nRADIO MODULE NOT CONNECTED\n")
	txfile.write("\nERROR 1: RADIO MODULE NOT CONNECTED\n")
	txfile.close()
	sys.exit(1) #1 means the radio module has a problem

#Defines I2C address of current sensors
try:
	ina219A = INA219(0x45)
	ina219B = INA219(0x41)
except:
	print("\nCURRENT SENSORS NOT CONNECTED\n")
	txfile.write("\nERROR 2: CURRENT SENSORS NOT CONNECTED\n")
	txfile.close()
	sys.exit(2) #2 means the current/power sensors have a problem
	
#GPIO INFO FOR PYROS
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, 0)

#define frame and frame structure
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

#define file path to read from config file
global path
path = "masterconfig.txt" #USE ABSOLUTE PATH WHEN KNOWN

#read values from config file
FRAMESIZE = int(configRead("FRAMESIZE"))
DECSIZE = int(configRead("DECSIZE"))
roundOff = int(configRead("roundOff"))
#flight variables that will be updated in get frame
global flightMode
flightMode = int(configRead("flightMode"))
global squibDeployed
squibDeployed = int(configRead("squibDeployed"))
global SQUIBDELAY
SQUIBDELAY = float(configRead("SQUIBDELAY"))
global delayStart
delayStart = float(configRead("delayStart"))
global ground
ground = int(configRead("ground"))
global apogeeReached
apogeeReached = int(configRead("apogeeReached"))
global passedCutoff #1000 m
passedCutoff = int(configRead("passedCutoff"))
global cutoff #right now 1000 m
cutoff = int(configRead("cutoff"))
altArray = []
corrAltArray = []
for i in range(2): #so that index errors don't occur
	altArray.append(0)
	corrAltArray.append(0)

#QNH used for setting altitude
if ground == 1:
	try:
		QNH = round(weather.pressure() / 100,2)
	except:
		QNH = -99999.0
	configWrite("QNH", QNH)
else:
	QNH = float(configRead("QNH"))

#kalman filter variables.  Note that pressure data is already filtered, this is extra on top of it
#read these from file
global k1 #initial value estimation
k1 = float(configRead("k1"))
global k2 #initial error estimation
k2 = float(configRead("k2"))
global k3 #process noise
k3 = float(configRead("k3"))
global k4 #sensor noise
k4 = float(configRead("k4"))
global k5 #initialize a variable used later
k5 = float(configRead("k5"))

#Send 2 frames
sendFrame()
sendFrame()
#locate self in code
flightMode = whereAmI()
configWrite("flightMode", flightMode)
while True:
	try:
		sendFrame()
		flightOperation(flightMode)
		#check for emergency chute deployment, in case something goes wrong, independent of flightmode
		if len(frame) > 10:
			if frame[-10]["altP"] > cutoff:
				passedCutoff = 1
				flightMode = 3
				configWrite("passedCutoff", passedCutoff)
				configWrite("flightMode", flightMode)
		if passedCutoff == 1 and frame[-1]["altP"] < cutoff and squibDeployed == 0:
			squibDeployed = 1
			flightMode = 5
			configWrite("squibDeployed", squibDeployed)
			configWrite("flightMode", flightMode)
			GPIO.output(20,1)
			GPIO.cleanup()		
			print("EMERGENCY DEPLOYMENT ACTIVATED")
			txfile.write("EMERGENCY DEPLOYMENT ACTIVATED")
			
	except(KeyboardInterrupt):
		gpsp.running = False
		gpsp.join()
		txfile.close()
		ser.close()

	#### ---------- End of Main Loop ---------- ####
