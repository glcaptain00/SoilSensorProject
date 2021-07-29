from datetime import datetime
from datetime import timedelta
from random import random
import sys

#Setup ranges
longRange = range(-500, 500, 10)
latRange = range(-500, 500, 10)
heightRange = range(9)

file = open("RandomGeneratedData2.csv", "w") #Open output file

file.write("Timestamp,RSSI,RelativeLatitude,RelativeLongitude,Height\n") #Write columns

def calcRSSI(lat, lng, height): #Define function to calculate RSSI based on position
    RSSI = -40-height*.075-abs(lat)*.06*((height/2)-1)-abs(lng)*.06*((height/2)-1) #Calculate RSSI
    if (RSSI < -110 or random() < 0.025): #If the calculated RSSI is too weak or a random packet loss is triggered
        #Note: random() returns a number between 0 and 1, not including 1. 
        #So checking to see if it's less than 0.025 is the equivalent of creating a 2.5% chance of packet loss
        return "Packet Loss"
    return RSSI

i = 0
#Three loops for iterating through the position
for h in heightRange:
    for lng in longRange:
        for lat in latRange:
            Height = h*3+3 #Calculate height
            file.write("{},{},{},{},{}\n".format(datetime.now() + timedelta(seconds=((i-1)/2)), calcRSSI(lat, lng, Height), lat, lng, Height)) #Output values
            i += 1
        
    
file.close()