import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=None)
string = "\x00ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKL"
ser.write(string)
ser.close()
