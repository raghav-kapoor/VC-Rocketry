import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
string = ""
while True: 
  print i
  ser.write(str(i))
ser.close()
