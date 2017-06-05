#!/usr/bin/python
 
from Subfact_ina219 import INA219

#Initialize current sensor objects with distinct i2c addresses  
ina1 = INA219(0x41)
ina5 = INA219(0x45)

#Test to make sure current sensors are properly initialized
result1 = ina1.getBusVoltage_V()
result5 = ina5.getBusVoltage_V()
 
#Input values from current sensor connected to LiPo battery
print "Shunt   0x41: %.3f mV" % ina1.getShuntVoltage_mV()
print "Bus     0x41: %.3f V" % ina1.getBusVoltage_V()
print "Current 0x41: %.3f mA" % ina1.getCurrent_mA()

print ""

#Input values from current sensor connected to 9V battery for pyros
print "Shunt   0x45: %.3f mV" % ina5.getShuntVoltage_mV()
print "Bus     0x45: %.3f V" % ina5.getBusVoltage_V()
print "Current 0x45: %.3f mA" % ina5.getCurrent_mA()

