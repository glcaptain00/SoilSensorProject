##########################################
# This file generates random RSSI values #
# and associates them with each line of  #
# the drone log files.                   #
########################################## 

from random import random

#Open files
file = open("droneDat.csv", "r")
out = open("output.csv", "w")


file.readline() #Read column headers
out.write("Time,RSSI,Latitude,Longitude,Height\n") #Write column headers

#For each line in the input file
for line in file:
    dat = line.split(",") #Split the data
    out.write("{},{},{},{},{}\n".format(dat[1], int(((random() * 50) + 40) * -1), dat[2], dat[3], dat[5])) #Write coordinates and random RSSI value between 40 and 90 to output
out.close()