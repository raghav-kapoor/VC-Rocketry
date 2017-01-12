import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600)
string = ""
for i in range(100): 
  print i
  ser.write(str(i))
ser.close()
