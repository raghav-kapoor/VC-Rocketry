import gps
from gps import *
import threading
import os
from subprocess import call
gpsd = None

call(["sudo", "systemctl", "stop", "gpsd.socket"])
call(["sudo", "systemctl", "disable", "gpsd.socket"])
call(["sudo", "gpsd", "/dev/ttyUSB0", "-F", "/var/run/gpsd.sock"])

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd #bring it in scope
        gpsd = gps(mode = WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True #setting the thread running to true
    def run(self):
        global gpsd
        while gpsp.running:
            gpsd.next()

if __name__ == '__main__':
    gpsp = GpsPoller()
    gpsp.start()
    go = True
    while go:
	print gpsd.fix.latitude
        if gpsd.fix.latitude != 0.0:
            go = False
            print("GPS Locked")
        else:
            time.sleep(0.5)
