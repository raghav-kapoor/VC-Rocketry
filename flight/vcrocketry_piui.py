# -*- coding: utf-8 -*-
import functools
import os
import random
import time
from piui import PiUi
 
current_dir = os.path.dirname(os.path.abspath(__file__))

#Variables:
a_x = -1
a_y = -1
a_z = -1
temp = -1
pressure = -1
volt_b1 = -1
current_1 = -1
volt_b2 = -1
current_2 = -1
gps_lat = -1
gps_lon = -1
gps_alt = -1
gps_spd = -1
mag_x = -1
mag_y = -1
mag_z = -1
 
#main class for webpage
class VCRocketry(object):
    #Initial empty page
    def __init__(self):
        self.title = None
        self.txt = None
        self.img = None
        self.ui = PiUi(img_dir=os.path.join(current_dir, 'imgs'))
 
    #Main info page
    def frameDisplay(self):
        self.page = self.ui.new_ui_page(title="VC Rocketry")
        self.list = self.page.add_list()
        self.list.add_item("a_x: ", get_a_x)
        self.list.add_item("a_y: ", get_a_y)
        self.list.add_item("a_z: ", get_a_z)
        self.list.add_item("temp: ", get_temp)
        self.list.add_item("pressure: ", get_pressure)
        self.list.add_item("volt_b1: ", get_volt_b1)
        self.list.add_item("current_1: ", get_current_1)
        self.list.add_item("volt_b2: ", get_volt_b2)
        self.list.add_item("current_2: ", get_current_2)
        self.list.add_item("gps_lat: ", get_gps_lat)
        self.list.add_item("gps_lon: ", get_gps_lon)
        self.list.add_item("gps_alt: ", get_gps_alt)
        self.list.add_item("gps_spd: ", get_gps_spd)
        self.list.add_item("mag_x: ", get_mag_x)
        self.list.add_item("mag_y: ", get_mag_y)
        self.list.add_item("mag_z: ", get_mag_z)
 
    #Methods for getting data from frame
    def get_a_x():
        return a_x
     
    def get_a_y():
        return a_y
     
    def get_a_z():
        return a_z
     
    def get_temp():
        return temp
     
    def get_pressure():
        return pressure
     
    def get_volt_b1():
        return volt_b1()
     
    def get_current_1():
        return current_1
     
    def get_volt_b2():
        return volt_b2
 
    def get_gps_lon():
        return gps_lon
 
    def get_gps_lat():
        return gps_lat
 
    def get_gps_alt():
        return gps_alt
 
    def get_gps_spd():
        return gps_spd
 
    def get_mag_x():
        return mag_x
 
    def get_mag_y():
        return mag_y
 
    def get_mag_z():
        return mag_z
def main():
    piui = DemoPiUi()
    piui.main()
 
if __name__ == '__main__':
    main()
