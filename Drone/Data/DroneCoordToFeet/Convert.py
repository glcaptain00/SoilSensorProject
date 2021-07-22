import math
import os

#CONSTANTS
earthRadius = 3958.8 #miles

dir = os.listdir()
for file in dir:
    if not (file.startswith("3-")):
        continue
    input = open(file, "r")
    output = open(file.replace("3-","4-"), "w")

    output.write(input.readline())

    def coordOffset(latOrLong): #Takes in either that latitude or longitude of a point and gives an approximate distance to that point in the same direction in feet.
        rad = latOrLong * (math.pi / 180)
        return rad * 3958.8 * 5280
        
        
    print(coordOffset(0.00005))


    for line in input:
        dat = line.split(",")
        latInFeet = coordOffset(float(dat[2]))
        longInFeet = coordOffset(float(dat[3]))
        output.write("{},{},{},{},{}".format(dat[0],dat[1],latInFeet,longInFeet,dat[4]))