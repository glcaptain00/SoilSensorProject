from random import random

file = open("droneDat.csv", "r")
out = open("output.csv", "w")

file.readline()
out.write("Time,RSSI,Latitude,Longitude,Height\n");

for line in file:
    dat = line.split(",")
    out.write("{},{},{},{},{}\n".format(dat[1], int(((random() * 50) + 40) * -1), dat[2], dat[3], dat[5]))
out.close()