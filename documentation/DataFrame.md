#Rocket Data Frame Structure
===========================

Structure (of one frame):
-------------------------
- "<" = start of new frame
- "," = end of value
- ">" = end of frame


Data Point entries:
-------------------
- **time-millisecond since epoch:**	13 digits
- **flight_mode:**	0-Ground mode unarmed; 1-Ground mode armed; 2-Flight mode ascend; 3-Flight mode descend; 4-Recovery mode
- **C-squib deployment:**	0-Not deployed; 1-Deployed
- **temp-temperature:**	in celceus
- **E-pressure:**	in 10 Pa
- **F-current 1:**	in mA
- **G-voltage 1:**	in V
- **H-current 2:**	in mA
- **I-voltage 2:**	in V
- **J-gps lat:**	in 0.000001 degrees, 10 digits (first digit positivity) PDDD(.)DDDDDD
- **K-gps long:**	in 0.000001 degrees, 10 digits (first digit positivity)
- **L-gps alt:**	in meters, 4 digits
- **M-gps speed:**	in 0.1 m/s, 4 digits
- **N-accelerometer x:**	in g
- **O-accelerometer y:**	in g
- **P-accelerometer z:**	in g
- **Q-magnetometer x:**	in 10 G
- **R-magnetometer y:**	in 10 G
- **S-magnetometer z:**	in 10 G

Datapoint:
----------
By point:	13	1	1	4	5	4	4	4	4	10	10	5	4	4	4	4	4	4	4			

Example:
--------
<128752648,0,0,20.8431	,10090,366,-1,0037275995,1121826885,143.3,1478309345067,0.458,1.1864,-1.4392,1.999,1395,-2182,-3231,>

<07AC9C08,0,0,32E2F,100909.83,366,-1,37.275995,-121.82688,143.3,1478309345067,0.458,1.1864,-1.4392,1.999,1395,-2182,-3231,>

999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
35F9DEA3E1F6BDFEF70CDD17B25EFA418CA63A22764CEC0FFFFFFFFFFFFFFFFFFFF
1EAE8CAEF261ACA01951E89D8FDC6C8F21DCE14E908133C599E12A9FFFFFFFFFFFFFFFFFFFFFFF
999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999