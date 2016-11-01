import time
from envirophat import motion
#Defining constant variables
#
#
#Time interval for acceleration calculations
TIME_INT = 0.1 

#Defining global variables before main loop
#
#
#
# class for axis
class Axis():
	#a, v, p from accelerometer
	aA = 0.0
	vA = 0.0
	pA = 0.0
	#lasest update time 
	tA = 0.0

	def __init__(self, aA, tA):
		self.aA = aA
		self.tA = tA

#Init axis objects
x = Axis(motion.accelerometer().x, time.time())
y = Axis(motion.accelerometer().y, time.time())
z = Axis(motion.accelerometer().z, time.time())

#Function for updating velocity and position from accelerometer
def velocityPositionFromAcceleration(Axis ax, float newA):
	tInt = time.time() - ax.tA
	ax.tA += tInt
	newV = (newA + ax.aA) * tInt / 2
	ax.pA = (newV + ax.vA) * tInt / 2
	ax.vA = newV
	ax.aA = newA

