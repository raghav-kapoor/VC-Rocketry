##Rocket Data Frame Structure
===========================

######Structure (of one frame):
-------------------------
- "<" = start of new frame
- "," = end of value
- ">" = end of frame


######Data Point entries:
-------------------
- A-linux time !
- B-flight mode: one character !
- C-squib deployment: 1 or 0 !
- D-temperature
- E-pressure
- F-current 1
- G-current 2
- H-gps lat
- I-gps long
- J-gps alt
- K-gps speed
- L-gps time 
- M-accelerometer x
- N-accelerometer y
- O-accelerometer z
- P-speed from accelerometer
- Q-mag x
- R-mag y
- S-mag z


######Example:
--------
> <1478128752648,0,0,20.8431,100909.83,366,-1,37.275995,-121.82688,J,K,L,1.1864,-1.4392,1.999,1395,-2182,-3231>
