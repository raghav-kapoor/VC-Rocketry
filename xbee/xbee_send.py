import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600)
string = ""
<<<<<<< HEAD
for i in range(10000000):
  print i 
=======
for i in range(100): 
  print i
>>>>>>> 391708f331a81236186868c18696e25d119aeeb2
  ser.write(str(i))
ser.close()
