#Rocket Data Frame Structure
===========================

Structure (of one frame):
-------------------------
- "<" = start of new frame
- "," = end of value
- ">" = end of frame


Data Point entries:
-------------------
- **A-linux time:** in milliseconds
- **B-flight mode:** 0-Ground mode; 1-Flight mode; 2-Recovery mode
- **C-squib deployment:** 0-Not deployed; 1-Deployed
- **D-temperature:** in celceus
- **E-pressure:** in Pa
- **F-current 1:** in mA
- **G-current 2:** in mA
- **H-gps lat:** in degrees
- **I-gps long:** in degrees
- **J-gps alt:** in meters
- **K-gps speed:** in m/s
- **L-gps time:** in milliseconds
- **M-accelerometer x:** in g
- **N-accelerometer y:** in g
- **O-accelerometer z:** in g
- **P-speed from accelerometer:** in  m/s
- **Q-mag x:** raw data?
- **R-mag y:** 
- **S-mag z:** 


Example:
--------
<1478128752648,0,0,20.8431,100909.83,366,-1,37.275995,-121.82688,143.3,1478309345067,0.458,1.1864,-1.4392,1.999,1395,-2182,-3231,>
