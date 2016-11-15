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

