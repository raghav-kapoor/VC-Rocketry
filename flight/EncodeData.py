import time

def binToAscii(x):
	if(len(x)%8!=0):
		for i in range((8-(len(str(x))%8))):
			x='0'+x
	split = [x[i:i+8] for i in range(0, len(x), 8)]
	asciiStr = ''
	for x in split:
		asciiStr+=chr(int(x, 2))
	return asciiStr

def asciiToBin(x):
	binStr = ''
	for i in x:
		binStr+=str(((bin(ord(i)))[2:]).zfill(8))
	return binStr

def decToBin(x):
	x = int(x)
	return(((str(bin(x)))[2:]).rstrip("L"))

def binToDec(x):
	return(str(int(str(x),2)))


testFrame = { 
	"time": time.time(),
	"flight_mode": 0,
	"squib_deployed": 0,
	"temp": 24.1167,
	"pressure": 100753.5629,
	"current_1": -519.0,
	"volt_b1": 3.84,
	"current_2": -1.0,
	"volt_b2": 1.024,
	"gps_lat": 37.275995,
	"gps_lon": -121.82688,
	"gps_alt": 143.3,
	"gps_spd": 1.999,
	"a_x": 0.0677,
	"a_y": -0.0447,
	"a_z": 1.0335,
	"mag_x": 1395,
	"mag_y": -2182,
	"mag_z": -3231 }

cFrame = ""
cFrame += str(int(testFrame["time"]*1000))
cFrame += str(testFrame["flight_mode"])
cFrame += str(testFrame["squib_deployed"])
cFrame += str(abs(int(testFrame["temp"]*10))+1000).zfill(4)[-4:]
cFrame += str(abs(int(testFrame["pressure"]/10))).zfill(5)[-5:]
cFrame += str(abs(int(testFrame["current_1"]*10))).zfill(4)[-4:]
cFrame += str(abs(int(testFrame["volt_b1"]*1000))).zfill(4)[-4:]
cFrame += str(abs(int(testFrame["current_2"]*10))).zfill(4)[-4:]
cFrame += str(abs(int(testFrame["volt_b2"]*1000))).zfill(4)[-4:]
cFrame += "0" + str(int(testFrame["gps_lat"]*1000000)).zfill(9)[-9:] if testFrame["gps_lat"] > 0 else "1" + str(abs(int(testFrame["gps_lat"]*1000000))).zfill(9)[-9:]
cFrame += "0" + str(int(testFrame["gps_lon"]*1000000)).zfill(9)[-9:] if testFrame["gps_lon"] > 0 else "1" + str(abs(int(testFrame["gps_lon"]*1000000))).zfill(9)[-9:]
cFrame += str(abs(int(testFrame["gps_spd"]*10))).zfill(4)[-4:]
cFrame += "0" + str(int(testFrame["a_x"]*10)).zfill(3)[-3:] if testFrame["a_x"] > 0 else "1" + str(abs(int(testFrame["a_x"]*10))).zfill(3)[-3:]
cFrame += "0" + str(int(testFrame["a_y"]*10)).zfill(3)[-3:] if testFrame["a_y"] > 0 else "1" + str(abs(int(testFrame["a_y"]*10))).zfill(3)[-3:]
cFrame += "0" + str(int(testFrame["a_z"]*10)).zfill(3)[-3:] if testFrame["a_z"] > 0 else "1" + str(abs(int(testFrame["a_z"]*10))).zfill(3)[-3:]
cFrame += "0" + str(int(testFrame["mag_x"]/10)).zfill(3)[-3:] if testFrame["mag_x"] > 0 else "1" + str(abs(int(testFrame["mag_x"]/10))).zfill(3)[-3:]
cFrame += "0" + str(int(testFrame["mag_y"]/10)).zfill(3)[-3:] if testFrame["mag_y"] > 0 else "1" + str(abs(int(testFrame["mag_y"]/10))).zfill(3)[-3:]
cFrame += "0" + str(int(testFrame["mag_z"]/10)).zfill(3)[-3:] if testFrame["mag_z"] > 0 else "1" + str(abs(int(testFrame["mag_z"]/10))).zfill(3)[-3:]

print cFrame
cFrameBin = decToBin(cFrame)
print cFrameBin
cFrameEncoded = binToAscii(cFrameBin)
print cFrameEncoded
print binToDec(asciiToBin(cFrameEncoded))

#1479020362719001241100755190384000101024003727599511218268800019000010000010013912191324
#10111110010101010110010001010111001101101110110100001100101000011000100100100111011110110010000100010110011100010110001010000011111110110110111111101100000001000111111101100011100110011100100001010001000100010101010100000110111001101110011111111110100100011100001000100101011101000101011100
