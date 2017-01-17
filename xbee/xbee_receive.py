import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600)  #timeout=None
out = ''
while True:
	out = ser.read(1)
	print 'Received %s' % out
ser.close()
