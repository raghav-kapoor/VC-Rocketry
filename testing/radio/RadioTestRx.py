import serial
import time
ser = serial.Serial('/dev/ttyUSB0', 9600)
outfile = open("reception" + str(time.time()) + ".txt", "w")

while True:
  try:
    line = ser.read(45) #should begin with AA, have 39 M's, and end with 4 numbers
    print(line)
    outfile.write(line)
  except KeyboardInterrupt:
    break
