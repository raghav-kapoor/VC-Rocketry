import time
import serial
import sys

ser = serial.Serial("/dev/ttyUSB0", 9600)
rxfile = open("testreceive.txt", "w")
FRAMESIZE= 39
DECSIZE = 93


def asciiToBin(x):
	binStr = ''
	for i in x:
		binStr+=str(((bin(ord(i)))[2:]).zfill(8))
	return binStr

def binToDec(x):
	return(str(int(str(x),2)))

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

def nicePrintout(data):
	print("\rTime: {0}".format(data["time"]), end = " ")
	print(" Flight mode: {0}".format(data["flight_mode"]), end = " ")
	print(" Squib Deployed: {0}".format(data["squib_deployed"]), end = " ")
	print(" Temperature: {0}".format(data["temp"]), end = " ")
	print(" Pressure: {0}".format(data["pressure"]), end = " ")
	print(" Current 1: {0}".format(data["current_1"]), end = " ")
	print(" Bus Voltage 1: {0}".format(data["volt_b1"]), end = " ")
	print(" Current 2: {0}".format(data["current_2"]), end = " ")
	print(" Bus Voltage 2: {0}".format(data["volt_b2"]), end = " ")
	print(" GPS Latitude: {0}".format(data["gps_lat"]), end = " ")
	print(" GPS Longitude: {0}".format(data["gps_lon"]), end = " ")
	print(" GPS Altitude: {0}".format(data["gps_alt"]), end = " ")
	print(" GPS Speed: {0}".format(data["gps_spd"]), end = " ")
	print(" Acceleration X: {0}".format(data["a_x"]), end = " ")
	print(" Acceleration Y: {0}".format(data["a_y"]), end = " ")
	print(" Acceleration Z: {0}".format(data["a_z"]), end = " ")
	print(" Magnetometer X: {0}".format(data["mag_x"]), end = " ")
	print(" Magnetometer Y: {0}".format(data["mag_y"]), end = " ")
	print(" Magnetometer Z: {0}".format(data["mag_z"]), end = " ")
	     
test={"time": 420, "flight_mode": 420, "squib_deployed": 420, "temp": 420, "pressure": 420, "current_1": 420, "volt_b1": 420, "current_2": 420, "volt_b2": 420, "gps_lat": 420, "gps_lon": 420, "gps_alt": 420, "gps_spd": 420, "a_x": 420, "a_y": 420, "a_z": 420, "mag_x": 420, "mag_y": 420, "mag_z": 420}

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
			rxfile.write(str(disassembledData))
			rxfile.write("\n")
			nicePrintout(disassembledData)
			fCount += 1
		    tempLine = ""
	except (KeyboardInterrupt):
		ser.close()
		rxfile.close()
