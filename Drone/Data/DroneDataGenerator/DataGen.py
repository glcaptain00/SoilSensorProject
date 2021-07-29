from datetime import datetime
from datetime import timedelta
from random import random
import sys


numpoints = 10000 #Default number of points to generate

if (sys.argv[1] != None): #If there is a command line argument
    try: 
        numpoints = int(sys.argv[1]) #Try to convert the first argument to a number
    except:
        print("Invalid number of points. Reverting to default.") #If it fails, revert to the default
     


file = open("RandomGeneratedData.csv", "w") #Open the output file

file.write("Timestamp,RSSI,RelativeLatitude,RelativeLongitude,Height\n") #Write columns

def calcRSSI(lat, long, height): #Define a function to calculate an RSSI value based on position
    RSSI = -40-height*.075-abs(lat)*.06*((height/2)-1)-abs(long)*.06*((height/2)-1) #Calculate RSSI
    if (RSSI < -110 or random() < 0.025): #If the calculated RSSI is too weak or a random packet loss is triggered
        #Note: random() returns a number between 0 and 1, not including 1. 
        #So checking to see if it's less than 0.025 is the equivalent of creating a 2.5% chance of packet loss
        return "Packet Loss"
    return RSSI


for i in range(numpoints): #For loop that iterates a number of times equal to the number of points desired
    #Calculate a random position
    Lat = (random()*1000)-500
    Long = (random()*1000)-500
    Height = int(random()*9)*3+3
    
    #Write position and calculated RSSI to the file
    file.write("{},{},{},{},{}\n".format(datetime.now() + timedelta(seconds=((i-1)/2)), calcRSSI(Lat, Long, Height), Lat, Long, Height))
    

file.close() #Close the file