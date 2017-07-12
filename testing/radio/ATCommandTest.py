import sys
import time
import os
import io
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.write("+++")
time.sleep(1)
ser.write("ATID") #ask for ID
reply = ""
char = ser.read()
while char != "\r":
  reply += char
  char = ser.read()
print(reply)
print(reply.decode("utf-8"))
ser.write("ATCN")

def readATParam(ser, name):  
  command = "AT" + name
  ser.write(command)
  reply = ""
  char = ser.read()
  while char != "\r":
    reply += char
    char = ser.read()
  return reply.decode("utf-8")

#ser.write("+++")
#time.sleep(1)
#readATParam(ser, ID)
#readATParam(ser, HC)
#readATParam(ser, MY)
#readATParam(ser, DT)
#readAtParam(ser, RS)
