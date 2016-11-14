#Rocket Data Frame Structure
===========================

Structure (of one frame):
-------------------------
- "<" = start of new frame
- "," = end of value
- ">" = end of frame


Data Point entries:
-------------------
- **A-linux time:**			 9 digits (First four digits on lauch day will always be 1479, thus not included.)
- **B-flight mode:**	0-Ground mode unarmed; 1-Ground mode armed; 2-Flight mode ascend; 4-Recovery mode
- **C-squib deployment:**	0-Not deployed; 1-Deployed
- **D-temperature:** in celceus			
- **E-pressure:** in Pa
- **F-current 1:** in mA
- **G-current 2:** in mA
- **H-gps lat:** in 0.000001 degrees, 10 digits (first digit positivity) PDDD(.)DDDDDD
- **I-gps long:** in 0.000001 degrees, 10 digits (first digit positivity)
- **J-gps alt:** in 0.1 meters, 4 digits
- **K-gps speed:** in 0.1 m/s, 4 digits
- **L-gps time:** in milliseconds 9 digits ignoring 1479
- **M-accelerometer x:** in g
- **N-accelerometer y:** in g
- **O-accelerometer z:** in g
- **P-mag x:** raw data?
- **Q-mag y:** 
- **R-mag z:** 

Datapoint:
----------
By point:	9	1	1	4	5	4	4	10	10	4	4	4	4	4	4	4	4
Verified:	9	1	1	4	5			10	10			4	4	4				

Example:
--------
<128752648,0,0,20.8431	,100909.83,366,-1,0037275995,1121826885,143.3,1478309345067,0.458,1.1864,-1.4392,1.999,1395,-2182,-3231,>

<07AC9C08,0,0,32E2F,100909.83,366,-1,37.275995,-121.82688,143.3,1478309345067,0.458,1.1864,-1.4392,1.999,1395,-2182,-3231,>

999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
35F9DEA3E1F6BDFEF70CDD17B25EFA418CA63A22764CEC0FFFFFFFFFFFFFFFFFFFF
1EAE8CAEF261ACA01951E89D8FDC6C8F21DCE14E908133C599E12A9FFFFFFFFFFFFFFFFFFFFFFF
999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999