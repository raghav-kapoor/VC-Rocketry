import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
out = ''
for i in range(100):
	out = ser.read(1)
	print 'Received %s' % out
ser.close()
