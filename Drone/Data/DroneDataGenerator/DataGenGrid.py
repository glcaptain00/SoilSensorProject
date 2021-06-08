from datetime import datetime
from datetime import timedelta
from random import random
import sys

longRange = range(-500, 500, 10)
latRange = range(-500, 500, 10)
heightRange = range(9)

file = open("RandomGeneratedData2.csv", "w")

file.write("Timestamp,RSSI,RelativeLatitude,RelativeLongitude,Height\n")

def calcRSSI(lat, long, height):
    RSSI = -40-height*.075-abs(lat)*.06*((height/2)-1)-abs(long)*.06*((height/2)-1)
    if (RSSI < -110 or random() < 0.025):
        return "Packet Loss"
    return RSSI

i = 0
for h in heightRange:
    for long in longRange:
        for lat in latRange:
            Height = h*3+3;
            Long = long
            Lat = lat
            file.write("{},{},{},{},{}\n".format(datetime.now() + timedelta(seconds=((i-1)/2)), calcRSSI(Lat, Long, Height), Lat, Long, Height)) 
            i += 1
        
    
file.close()