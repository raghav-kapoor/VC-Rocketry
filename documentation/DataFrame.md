#Rocket Data Frame Structure
===========================

Structure (of one frame):
-------------------------
The structure of the frame is basically a string of pure decimal digits. For easy conversion, there is no divider between each data point entry, and thus they're identified solely from the position of each digit since each entry is always formatted into the same exact length.

Since our radio module function takes in ASCII character, and for the purpose of representing more data and fully utilizing all 256 ASCII character for the data transmission, we convert the string of numbers into binary, and use ASCII character to represent every 8 binary digits. The final string to be sent consists ASCII characters, and we add four dollar signs ("$$$$") in the end to represent end of a frame.

Data Point entries:
-------------------
Each entry in rounded to be the shortest but best representation of the respective sensor accuracy. (Which I tasked @vminh1999 so hard on lmao.)
There are two types of entry: with or without positivity.
The ones with positivity has a header digit (the first digit) that represents the data's positivity.
- 0 means it's positive, 1 means it's negative

Here are the specifics of each point:

- **time-millisecond since epoch:**	13 digits - No positivity
- **flight_mode:**	0-Ground mode unarmed; 1-Ground mode armed; 2-Flight mode ascend; 3-Flight mode descend; 4-Recovery mode - No positivity
- **C-squib deployment:**	0-Not deployed; 1-Deployed - No positivity
- **temp-temperature:**	in celceus - No positivity
- **E-pressure:**	in 10 Pa - No positivity
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
By point:	13	1	1	4	5	4	4	4	4	10	10	5	4	4	4	4	4	4	4			<--- What is this?

Example:
--------
[] yet to be added

Some scratch stuff :/
---------------------
<128752648,0,0,20.8431	,10090,366,-1,0037275995,1121826885,143.3,1478309345067,0.458,1.1864,-1.4392,1.999,1395,-2182,-3231,>

<07AC9C08,0,0,32E2F,100909.83,366,-1,37.275995,-121.82688,143.3,1478309345067,0.458,1.1864,-1.4392,1.999,1395,-2182,-3231,>

999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
35F9DEA3E1F6BDFEF70CDD17B25EFA418CA63A22764CEC0FFFFFFFFFFFFFFFFFFFF
1EAE8CAEF261ACA01951E89D8FDC6C8F21DCE14E908133C599E12A9FFFFFFFFFFFFFFFFFFFFFFF
999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
