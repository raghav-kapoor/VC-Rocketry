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

testFrame = { 
	"time": time.time(),
	"flight_mode": 0,
	"squib_deployed": 0,
	"temp": 24.1167,
	"pressure": 100753.5629,
	"current_1": -519.0,
	"volt_b1": 3.84,
	"current_2": -1.0,
	"volt_b2": 1.024,
	"gps_lat": 37.275995,
	"gps_lon": -121.82688,
	"gps_alt": 143.3,
	"gps_spd": 1.999,
	"a_x": 0.0677,
	"a_y": -0.0447,
	"a_z": 1.0335,
	"mag_x": 1395,
	"mag_y": -2182,
	"mag_z": -3231 }

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

num = 0
while True:
    try:
        dataline = ser.read(FRAMESIZE)
        decodedData = bintoDec(asciiToBin(dataLine))
        disassembledData = frameDisassembly(decodedData)
        rxfile.write(disassembledData)
        rxfile.write("\n")
        print(size)
        print(disassembledData)
        num+=1
    except (KeyboardInterrupt):
        ser.close()
        rxfile.close()
        break

