
#!/usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(20,GPIO.OUT)

while True:
	try:
		state = (raw_input("On or Off:\n")).lower()

		if state == "on":
			print "Pin 40 on"
			GPIO.output(20,GPIO.HIGH)
		else:
			print "Pin 40 off"
			GPIO.output(20,GPIO.LOW)
	except KeyboardInterrupt:
		break
