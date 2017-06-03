import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600)
message = "AA"
message = message + "M" * 39
count=0
while True:
  try:
    count++
    tempMessage = message + str(count).zfill(4)
    ser.write(tempMessage)
    time.sleep(0.04)
  except KeyboardInterrupt:
    break
