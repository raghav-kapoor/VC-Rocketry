# -*- coding: utf-8 -*-

import time
import serial
import sys
import math

from EncodeData import decodeFrame

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
                    decodedFrame = decodeFrame(binToDec(asciiToBin(tempLine[:-2])))
                    #rxfile.write(str(decodedFrame))
                    #rxfile.write("\n")
                    frames.append(decodedFrame)
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
            a_x = decodedFrame["a_x"],
            a_y = decodedFrame["a_y"],
            a_z = decodedFrame["a_z"],
            temp = decodedFrame["temp"],
            pressure = decodedFrame["pressure"],
            current_1 = decodedFrame["current_1"],
            volt_b1 = decodedFrame["volt_b1"],
            current_2 = decodedFrame["current_2"],
            volt_b2 = decodedFrame["volt_b2"],
            gps_lon = decodedFrame["gps_lon"],
            gps_lat = decodedFrame["gps_lat"],
            gps_alt = decodedFrame["gps_alt"],
            gps_spd = decodedFrame["gps_spd"],
            mag_x = decodedFrame["mag_x"],
            mag_y = decodedFrame["mag_y"],
            mag_z = decodedFrame["mag_z"],
            angle = 90-math.atan((decodedFrame["mag_y"])/(decodedFrame["mag_x"]))*180/(3.14)
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
