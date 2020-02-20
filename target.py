import math
from datetime import datetime

def to_angle(deg, minute):
  deg = float(deg)
  minute = float(minute)
  if (deg >= 0.0):
    return (deg + minute/60.0)
  return (deg - minute/60.0)

def format_lat(deg):
  return "{:02d}{:06.3f}".format(int(deg), deg%1*60) 

def format_lon(deg):
  return "{:03d}{:06.3f}".format(int(deg), deg%1*60) 

#print format_lon(to_angle(45, 0.7))
#print format_lon(to_angle(5, 30.7))
#print format_lon(to_angle(45, 30.7))
#print format_lon(to_angle(145, 58.332))

class Target:
  def __init__(self, lat, lon, course, speed):
    """
    Construct a new 'Target' object.

    Parameters
    ----------
    lat: float
      latitude in degres. Positive north
    lon: float
      longitude in degres. Positive east
    course: float
      course over ground in degres, used for position update : 0.0 = north, 90.0 = east, 180.0 = south, 270.0 = west
    speed: float
      speed in knots
    """
    self.lat = lat
    self.lon = lon
    self.course = course
    self.speed = speed
    self.datetime = datetime.now()
  def update(self):
    """
    Updates the position since last update
    uses the real time difference
    """
    lat_a = self.lat
    lon_a = self.lon
    new_time = datetime.now()
    dur = (new_time - self.datetime).total_seconds()
    lat_b = lat_a + (self.speed * (dur/3600.0)
                      * math.cos(math.radians(self.course))
                      / 60.0)
    lat_m = (lat_a + lat_b)/2
    lon_b = lon_a + (self.speed * (dur/3600.0)
                      * math.sin(math.radians(self.course))
                      / math.cos(math.radians(lat_m)) / 60.0)
    self.lat = lat_b
    self.lon = lon_b
    self.datetime = new_time    

