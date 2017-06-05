import sys
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 9600)

goodFrame = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklx"
badFrame = "ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijkx"
reallyBadFrame = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijx"

start = "\x7F"
end = "\x00"

ser.write(goodFrame) #nothing should happen
time.sleep(0.5)
ser.write(start*2 + goodFrame + end*2) #ideal situation
time.sleep(0.5)
ser.write(start + goodFrame + start + goodFrame + end) #1 DEL detected twice
time.sleep(0.5)
ser.write(start*2 + badFrame + end*2) #frame wrong size
time.sleep(0.5)
ser.write(start*2 + goodFrame + end + start*2 + goodFrame + end*2) #2 NULL not detected, frame wronng size
time.sleep(0.5)
ser.write(start*50) #what will happen?
time.sleep(0.5)
ser.write(end*10) #what will happen?
time.sleep(0.5)
ser.write(start*2 + goodFrame + end*2) #is this still read as a good frame?
time.sleep(0.5)
