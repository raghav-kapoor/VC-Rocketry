import serial
import sys
import time

ser = serial.Serial("/dev/ttyUSB0", 9600)
target = open("test.txt", "w")
frameSize = 37

def asciiToBin(x):
	binStr = ''
	for i in x:
		binStr+=str(((bin(ord(i)))[2:]).zfill(8))
	return binStr

def binToDec(x):
	return(str(int(str(x),2)))

while True:
    outline = ser.read(37)
    binLine = binToDec(asciiToBin(outline))
    #decode to frame here

    target.write(binLine)
    target.write("\n")

class dataPoint:
	#name in dictionary
	name = ""
	#head digit for positivity
	hasHead = 0
	#amount of digits including the head
	length = 0
	#digits decimal offset count
	decOffset = 0

	def __init__(self, name, hasHead, length, decOffset):
		self.name = name
		self.hasHead = hasHead
		self.length = length
		self.decOffset = decOffset

def decode():
	frameStruct = []
	frameStruct.append(dataPoint("time", 0, 13, 0))
	frameStruct.append(dataPoint("flight_mode", 0, 1, 0))
	frameStruct.append(dataPoint("squib_deployed", 0, 1, 0))
	frameStruct.append(dataPoint("temp", 0, 4, 1))
	frameStruct.append(dataPoint("pressure", 0, 5, -1))
	frameStruct.append(dataPoint("current_1", 0, 4, 1))
	frameStruct.append(dataPoint("volt_b1", 0, 4, 4))
	frameStruct.append(dataPoint("current_2", 0, 4, 1))
	frameStruct.append(dataPoint("volt_b2", 0, 4, 4))
	frameStruct.append(dataPoint("gps_lat", 1, 10, 6))
	frameStruct.append(dataPoint("gps_lon", 1, 10, 6))
	frameStruct.append(dataPoint("gps_alt", 0, 5, 1))
	frameStruct.append(dataPoint("gps_spd", 0, 4, 1))
	frameStruct.append(dataPoint("a_x", 1, 3, 1))
	frameStruct.append(dataPoint("a_y", 1, 3, 1))
	frameStruct.append(dataPoint("a_z", 1, 3, 1))
	frameStruct.append(dataPoint("mag_x", 1, 3, -1))
	frameStruct.append(dataPoint("mag_y", 1, 3, -1))
	frameStruct.append(dataPoint("mag_z", 1, 3, -1))

	

def decodeBad():
    #framesGround = []
    #while(True):
    frame = {}
    frame["mag_z"] = x[88:]
    frame["mag_y"] = x[84:88]
    frame["squib_deployed"] = x[14:15]
    frame["flight_mode"] = x[13:14]
    frame["time"] = x[:13]
    #framesGround.append(frame)
    return frame 
    frame["mag_x"] = x[80:84]
    frame["a_z"] = x[76:80]
    frame["a_y"] = x[72:76]
    frame["a_x"] = x[68:72]
    frame["gps_spd"] = x[64:68]
    frame["gps_lat"] = x[40:50]
    frame["volt_b2"] = x[36:40]
    frame["current_2"] = x[32:36]
    frame["volt_b1"] = x[28:32]
    frame["current_1"] = x[24:28]
    frame["pressure"] = x[19:24]
    frame["temp"] = x[15:19]
    frame["gps_alt"] = x[60:64]
    frame["gps_lon"] = x[50:60]
