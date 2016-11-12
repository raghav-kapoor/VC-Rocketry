import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600)
string = "A" * 1000
for i in range(10):
  ser.write(string)
