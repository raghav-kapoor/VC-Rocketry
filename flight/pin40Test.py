from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
try:
	while True:
		GPIO.output(21, 1)
		print "on"
		sleep(1)
		#GPIO.output(21, 0)
		print "off"
		sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
