#open pipe
socat -d -d pty,raw,echo=0 pty,raw,echo=0

this will give two pts connected by a pipe

modify gps.py to set initial position and speed

then run gps.py and redirect output to one pts.

set opencpn to read nmea data from other side (the pts is not listed. must be entered manually)
