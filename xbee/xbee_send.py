import serial
from time import sleep
<<<<<<< HEAD
ser = serial.Serial('/dev/ttyUSB0', 9600)
<<<<<<< HEAD
string = "" 
for i in range(100): 
=======
string = ""
for i in range(1000000): 
>>>>>>> a6d5ce9cd3292177f830a2f4beed2e497edfb116
=======
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
string = ""
while True: 
>>>>>>> 5bd4695af2e207304798c76477990ba6015501d9
  print i
  ser.write(str(i))
ser.close()
