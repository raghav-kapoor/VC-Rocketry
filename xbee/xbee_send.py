import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600)
<<<<<<< HEAD
string = "" 
for i in range(100): 
=======
string = ""
for i in range(1000000): 
>>>>>>> a6d5ce9cd3292177f830a2f4beed2e497edfb116
  print i
  ser.write(str(i))

