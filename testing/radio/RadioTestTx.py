import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600)
message = "AA"
message = message + "M" * 39
message = message + "ZZ"
while True:
  try:
    ser.write(message)
    time.sleep(0.04)
  except KeyboardInterrupt:
    break
