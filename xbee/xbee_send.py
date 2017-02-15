import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600)
string = ""
for i in range(10000000): 
  print i
  if (i%1 == 0):
    ser.write(i)
 ser.close()
