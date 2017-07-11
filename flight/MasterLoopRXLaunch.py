# -*- coding: utf-8 -*-

import time
import serial
import sys
import math

ser = serial.Serial("/dev/ttyUSB0", 9600)
rxfile = open("testreceive.txt", "w")
FRAMESIZE= 39
DECSIZE = 93

#Converts ascii frames to binary
def asciiToBin(x):
	binStr = ''
	for i in x:
		binStr+=str(((bin(ord(i)))[2:]).zfill(8))
	return binStr

#Converts binary frames to decimal
def binToDec(x):
	return(str(int(str(x),2)))

# Function displaying frames in an orderly fashion
def write(line):
	sys.stdout.write(line)
	sys.stdout.flush()

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

def frameDisassembly(decAssembly):
	if (len(decAssembly) != DECSIZE):
		return "FrameWrongSize\n"
	cFrame = {}
	for dataPoint in FRAME_STRUCT:	
		if dataPoint.hasPositivity:
			cFrame[dataPoint.name] = (int(decAssembly[0:1])*-2+1) * int(decAssembly[1:dataPoint.length]) * (float(10**dataPoint.decOffset))
		else:
			cFrame[dataPoint.name] = (int(decAssembly[0:dataPoint.length]) * (float(10**dataPoint.decOffset)))
		
		decAssembly = decAssembly[dataPoint.length:]
	return cFrame

FRAME_STRUCT = []
FRAME_STRUCT.append(DataPoint("time", 0, 13, -3))
FRAME_STRUCT.append(DataPoint("flight_mode", 0, 1, 0))
FRAME_STRUCT.append(DataPoint("squib_deployed", 0, 1, 0))
FRAME_STRUCT.append(DataPoint("temp", 0, 4, -1))
FRAME_STRUCT.append(DataPoint("pressure", 0, 5, 1))
FRAME_STRUCT.append(DataPoint("current_1", 0, 4, -1))
FRAME_STRUCT.append(DataPoint("volt_b1", 0, 4, -3))
FRAME_STRUCT.append(DataPoint("current_2", 0, 4, -1))
FRAME_STRUCT.append(DataPoint("volt_b2", 0, 4, -3))
FRAME_STRUCT.append(DataPoint("gps_lat", 1, 10, -6))
FRAME_STRUCT.append(DataPoint("gps_lon", 1, 10, -6))
FRAME_STRUCT.append(DataPoint("gps_alt", 0, 5, -1))
FRAME_STRUCT.append(DataPoint("gps_spd", 0, 4, -1))
FRAME_STRUCT.append(DataPoint("a_x", 1, 4, -1))
FRAME_STRUCT.append(DataPoint("a_y", 1, 4, -1))
FRAME_STRUCT.append(DataPoint("a_z", 1, 4, -1))
FRAME_STRUCT.append(DataPoint("mag_x", 1, 4, 1))
FRAME_STRUCT.append(DataPoint("mag_y", 1, 4, 1))
FRAME_STRUCT.append(DataPoint("mag_z", 1, 4, 1))

frames = []
fCount = 0

while True:
	try:
	    tempLine = ""
	    if (ser.read(1) == "\x7F"):
		if (ser.read(1) == "\x7F"):
		    tempLine += ser.read(2)
		    while ((tempLine[-1] != "\x00" or tempLine[-2] != "\x00") and len(tempLine) < (FRAMESIZE + 2)):
			tempLine+=ser.read(1)
		    if (tempLine[-1] == "\x00" and tempLine[-2] == "\x00" and len(tempLine) == (FRAMESIZE + 2)):
			decodedData = binToDec(asciiToBin(tempLine[:-2]))
			disassembledData = frameDisassembly(decodedData)
			for key in disassembledData.keys():
				disassembledData[key] = round(disassembledData[key], 3)
			#rxfile.write(str(disassembledData))
			#rxfile.write("\n")
			frames.append(disassembledData)
			output = """
a_x: {a_x}g
a_y: {a_y}g
a_z: {a_z}g
temp: {temp}°C
pressure: {pressure}hPa
current_1: {current_1}mA
volt_b1: {volt_b1}V
current_2: {current_2}mA
volt_b2: {volt_b2}V
gps_lon: {gps_lon}
gps_lat: {gps_lat}
gps_alt: {gps_alt}m
gps_spd: {gps_spd}m/s
mag_x: {mag_x} Gauss
mag_y: {mag_y} Gauss
mag_z: {mag_z} Gauss
angle: {angle}degrees
""".format(
			a_x = disassembledData["a_x"],
			a_y = disassembledData["a_y"],
			a_z = disassembledData["a_z"],
			temp = disassembledData["temp"],
			pressure = disassembledData["pressure"],
			current_1 = disassembledData["current_1"],
			volt_b1 = disassembledData["volt_b1"],
			current_2 = disassembledData["current_2"],
			volt_b2 = disassembledData["volt_b2"],
			gps_lon = disassembledData["gps_lon"],
			gps_lat = disassembledData["gps_lat"],
			gps_alt = disassembledData["gps_alt"],
			gps_spd = disassembledData["gps_spd"],
			mag_x = disassembledData["mag_x"],
			mag_y = disassembledData["mag_y"],
			mag_z = disassembledData["mag_z"],
			angle = 90-math.atan((disassembledData["mag_y"])/(disassembledData["mag_x"]))*180/(3.14)
    	)
			output = output.replace("\n","\n\033[K")
                        write(output)
                        lines = len(output.split("\n"))
                        write("\033[{}A".format(lines - 1))
                        fCount += 1
                tempLine = ""
	except (KeyboardInterrupt):
		ser.close()
		rxfile.close()
