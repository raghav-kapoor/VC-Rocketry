import sys
from time import sleep
from Subfact_ina219 import INA219
import RPi.GPIO as GPIO

ina219A = INA219(0x40)
roundOff = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
try:
	while True:
		GPIO.output(20, 1)
		print "on"
		print("Voltage:  " + str(round(ina219A.getBusVoltage_V(), roundOff)))
		print("Current:  " + str(round(ina219A.getCurrent_mA(), roundOff)))
		sleep(1)
		GPIO.output(20, 0)
		print "off"
		print("Voltage:  " + str(round(ina219A.getBusVoltage_V(), roundOff)))
		print("Current:  " + str(round(ina219A.getCurrent_mA(), roundOff)))
		sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
