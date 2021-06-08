from datetime import datetime
from datetime import timedelta
from random import random
import sys


numpoints = 10000

if (sys.argv[1] != None):
    try:
        numpoints = int(sys.argv[1])
    except:
        print("Invalid number of points. Reverting to default.")
     


file = open("RandomGeneratedData.csv", "w")

file.write("Timestamp,RSSI,RelativeLatitude,RelativeLongitude,Height\n")

def calcRSSI(lat, long, height):
    RSSI = -40-height*.075-abs(lat)*.06*((height/2)-1)-abs(long)*.06*((height/2)-1)
    if (RSSI < -110 or random() < 0.025):
        return "Packet Loss"
    return RSSI


for i in range(numpoints):
    Lat = (random()*1000)-500
    Long = (random()*1000)-500
    Height = int(random()*9)*3+3
    file.write("{},{},{},{},{}\n".format(datetime.now() + timedelta(seconds=((i-1)/2)), calcRSSI(Lat, Long, Height), Lat, Long, Height))
    
file.close()