import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600,timeout=0)
string = 'H'
ser.write('%s' % string)

