import functools
import math
from time import sleep
from piui import PiUi

global flightMode
flightMode = 0
global squibDeployed
squibDeployed = 0

class RocketPiUi(object):

    def __init__(self):
        self.title = None
        self.txt = None
        self.img = None
        self.ui = PiUi()

    def main_page(self):
        self.page = self.ui.new_ui_page(title="VC Rocketry Live Update")

        self.page.add_textbox("Location", "h1")
        update1 = self.page.add_textbox("0.0, 0.0", "p")
        self.page.add_element("hr")

        self.page.add_textbox("Speed and Acceleration", "h1")
        update2 = self.page.add_textbox("Speed: 0.0, Acceleration: 0.0", "p")
        self.page.add_element("hr")

        self.page.add_textbox("Rocket Mode", "h1")
        update3 = self.page.add_textbox("Prechecks")
        self.page.add_element("hr")

        self.page.add_textbox("Squib Status", "h1")
        update4 = self.page.add_textbox("Not Deployed")
        self.page.add_element("hr")

        self.page.add_textbox("9 Volt Current Flowing", "h1")
        update5 = self.page.add_textbox("False")
        self.page.add_element("hr")

        for i in range(0, 50):
            # latitude = frame[-1]["latitude"]
            # longitude = frame[-1]["longitude"]
            # speed = frame[-1]["speed"]
            # acceleration = math.sqrt((frame[-1]["a_x"]*9.81)**2 + (frame[-1]["a_y"]*9.81)**2 + (frame[-1]["a_z"]*9.81)**2)
            # global flightMode
            # global squibDeployed
            # current = frame[-1]["current_1"]

            # This is dummy data, remove these varibales and uncomment the ones above for real testing
            # You will, of course, have to remove this code from the for loop
            flightMode = i
            squibDeployed = i
            x = float(i)
            latitude = x
            longitude = x
            speed = x
            acceleration = x
            current = x

            update1.set_text(str(latitude) + ", " + str(longitude))

            update2.set_text("Speed: " + str(speed) + " ft/s" + ", Acceleration: " + str(acceleration) + " m/s^2")

            if flightMode == 0:
                update3.set_text("Pre-Check 1")
            elif flightMode == 1:
                update3.set_text("Pre-Check 2")
            elif flightMode == 2:
                update3.set_text("Flight")
            elif flightMode == 3:
                update3.set_text("Descent")
            elif flightMode == 4:
                update3.set_text("Recovery")

            if squibDeployed == 1:
                update4.set_text("Deployed")

            if (current > 0.0):
                update5.set_text("True")
            else:
                update5.set_text("False")
            sleep(1)

        self.ui.done()

    def main(self):
        self.main_page()
        self.ui.done()

def main():
  piui = RocketPiUi()
  piui.main()

if __name__ == '__main__':
    main()

# for i in range(0, 50):
#     # latitude = frame[-1]["latitude"]
#     # longitude = frame[-1]["longitude"]
#     # speed = frame[-1]["speed"]
#     # acceleration = math.sqrt((frame[-1]["a_x"]*9.81)**2 + (frame[-1]["a_y"]*9.81)**2 + (frame[-1]["a_z"]*9.81)**2)
#     # global flightMode
#     # global squibDeployed
#     # current = frame[-1]["current_1"]
#     x = float(i)
#     latitude = x
#     longitude = x
#     speed = x
#     acceleration = x
#     current = x
#
#     update1.set_text(str(latitude) + ", " + str(longitude))
#
#     update2.set_text("Speed: " + str(speed) + " ft/s" + ", Acceleration: " + str(acceleration) + " m/s^2")
#
#     if flighMode == 0:
#         update3.set_text("Pre-Check 1")
#     elif flighMode == 1:
#         update3.set_text("Pre-Check 2")
#     elif flighMode == 2:
#         update3.set_text("Flight")
#     elif flighMode == 3:
#         update3.set_text("Descent")
#     elif flighMode == 4:
#         update3.set_text("Recovery")
#
#     if squibDeployed == 1:
#         update4.set_text("Deployed")
#
#     if (current > 0.0):
#         update5.set_text("True")
#     else:
#         update5.set_text("False")
#     sleep(1)
