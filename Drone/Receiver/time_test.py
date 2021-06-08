import sys
import os
import time
from datetime import datetime

print("Setting System Clock")

#Example given on NMEA website for $GPGGA message
sampleTime = "172814.0"
systemTime = datetime.utcnow()

month = systemTime.month
day = systemTime.day
hours = sampleTime[0:2]
minutes = sampleTime[2:4]
year = systemTime.year
seconds = sampleTime[4:6]


#print("Hours: %s\nMinutes: %s\nSeconds: %s" % (hours, minutes, seconds))


print("Time before: {}".format(systemTime))
os.system("sudo date -u {:0>2d}{:0>2d}{}{}{}.{}".format(month, day, hours, minutes, year, seconds))
print("Time after: {}".format(datetime.utcnow()))
