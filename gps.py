#!/usr/bin/python
import math
import time
import pynmea2
from datetime import datetime

def to_angle(deg, minute):
  return deg + minute/60

def format_lat(deg):
  return "{:02d}{:06.3f}".format(int(deg), deg%1*60) 

def format_lon(deg):
  return "{:03d}{:06.3f}".format(int(deg), deg%1*60) 

#print format_lon(to_angle(45, 0.7))
#print format_lon(to_angle(5, 30.7))
#print format_lon(to_angle(45, 30.7))
#print format_lon(to_angle(145, 58.332))

# initial positiona (degres, minutes)
lat_a = to_angle(48, 16.059)
lon_a = to_angle(4, 50.749)
lat_dir = 'N'
lon_dir = 'W'

# course and speed
speed = 5.0
course = 250.0

#delay in seconds
delay = 2.0

# format for NMEA sentences
speedS = "{:4.1f}".format(speed)
true_course = "{:.1f}".format(course)


while True:
  #timestamp = '184353.07' # hhmmss.ss UTC
  now = datetime.now()
  timestamp = now.strftime("%H%M%S.00")
  #date = '150220' # ddmmyy
  date = now.strftime("%d%m%y")
  
  lat = format_lat(lat_a)    # ddmm.mmm
  lon = format_lon(lon_a)    # dddmm.mmm 

  #$GPGGA,212005.030,4816.059,N,00450.739,W,1,12,1.0,0.0,M,0.0,M,,*70
  # GGA Global Positioning System Fix Data. Time, Position and fix related data for a GPS receiver
  #        ('Timestamp', 'timestamp', timestamp), hhmmss.ss
  #        ('Latitude', 'lat'), llll.ll
  #        ('Latitude Direction', 'lat_dir'), N S
  #        ('Longitude', 'lon'), yyyyy.yy
  #        ('Longitude Direction', 'lon_dir'), E W
  #        ('GPS Quality Indicator', 'gps_qual', int), 1 - GPS Fix
  #        ('Number of Satellites in use', 'num_sats'), 04
  #        ('Horizontal Dilution of Precision', 'horizontal_dil'), x.x (2.6)
  #        ('Antenna Alt above sea level (mean)', 'altitude', float), x.x (10.0)
  #        ('Units of altitude (meters)', 'altitude_units'), M
  #        ('Geoidal Separation', 'geo_sep'), xx.x 
  #        ('Units of Geoidal Separation (meters)', 'geo_sep_units'), M
  #        ('Age of Differential GPS Data (secs)', 'age_gps_data'), ''
  #        ('Differential Reference Station ID', 'ref_station_id'), '0000'
  
  msg = pynmea2.GGA('GP', 'GGA', (timestamp, lat, lat_dir, lon, lon_dir, '1', '04', '2.6', '100.00', 'M', '-33.9', 'M', '', '0000'))
  print str(msg)
  
  #$GPGSA,A,3,01,02,03,04,05,06,07,08,09,10,11,12,1.0,1.0,1.0*30
  # GSA = GPS DOP and active satellites
  #        ('Mode', 'mode'), A
  #        ('Mode fix type', 'mode_fix_type'),
  #        ('SV ID01', 'sv_id01'),
  #        ('SV ID02', 'sv_id02'),
  #        ('SV ID03', 'sv_id03'),
  #        ('SV ID04', 'sv_id04'),
  #        ('SV ID05', 'sv_id05'),
  #        ('SV ID06', 'sv_id06'),
  #        ('SV ID07', 'sv_id07'),
  #        ('SV ID08', 'sv_id08'),
  #        ('SV ID09', 'sv_id09'),
  #        ('SV ID10', 'sv_id10'),
  #        ('SV ID11', 'sv_id11'),
  #        ('SV ID12', 'sv_id12'),
  #        ('PDOP (Dilution of precision)', 'pdop'),
  #        ('HDOP (Horizontal DOP)', 'hdop'),
  #        ('VDOP (Vertical DOP)', 'vdop'),
  
  msg = pynmea2.GSA('GP', 'GSA', ('A','3','01','02','03','04','05','06','07','08','09','10','11','12','1.0','1.0','1.0'))
  print str(msg)
  
  #$GPRMC,212005.030,A,4816.059,N,00450.739,W,14268.3,092.9,150220,000.0,W*68
  # RMC = Recommended Minimum Navigation Information
  #        ("Timestamp", "timestamp", timestamp),
  #        ('Status', 'status'), # contains the 'A' or 'V' flag
  #        ("Latitude", "lat"),
  #        ("Latitude Direction", "lat_dir"),
  #        ("Longitude", "lon"),
  #        ("Longitude Direction", "lon_dir"),
  #        ("Speed Over Ground", "spd_over_grnd", float), x.x knots
  #        ("True Course", "true_course", float),
  #        ("Datestamp", "datestamp", datestamp), ddmmyy
  #        ("Magnetic Variation", "mag_variation"), x.x
  #        ("Magnetic Variation Direction", "mag_var_dir"), E W
  msg = pynmea2.RMC('GP', 'RMC', (timestamp, 'A', lat, lat_dir, lon, lon_dir, speedS, true_course, date, '0.0', 'E'))
  print str(msg)
  
  time.sleep(delay)

  if lat_dir == 'S':
    lat_a = -lat_a

  if lon_dir == 'W':
    lon_a = -lon_a

  lat_b = lat_a + speed * (delay/3600.0) * math.cos(math.radians(course))/60.0
  lat_m = (lat_a + lat_b)/2
  lon_b = lon_a + speed * (delay/3600.0) * math.sin(math.radians(course)) / math.cos(math.radians(lat_m)) / 60.0
  #print format_lat(lat_a)
  #print format_lat(lat_b)
  #print format_lon(lon_a)
  #print format_lon(lon_b)
  lat_a = lat_b
  lon_a = lon_b

  if lat_a < 0:
    lat_a = -lat_a
    lat_dir = 'S'
  else:
    lat_dir = 'N'

  if lon_a < 0:
    lon_a = -lon_a
    lon_dir = 'W'
  else:
    lon_dir = 'E'
