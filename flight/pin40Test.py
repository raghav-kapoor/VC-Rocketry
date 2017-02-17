from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
try:
	while True:
		GPIO.output(20, 1)
		print "on"
		sleep(1)
		GPIO.output(20, 0)
		print "off"
		sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
