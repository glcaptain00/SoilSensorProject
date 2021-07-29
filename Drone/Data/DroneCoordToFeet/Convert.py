import math
import os

#CONSTANTS
earthRadius = 3958.8 #miles

dir = os.listdir() #Get all files in the directory

def coordOffset(latOrLong): #Takes in either that latitude or longitude of a point and gives an approximate distance to that point in the same direction in feet.
        rad = latOrLong * (math.pi / 180) #Calculate the angle between the current point and 0. By this stage, all coordinates should be relative
        return rad * 3958.8 * 5280 #Return the arc length in feet. theta * radius * conversion

for file in dir: #For each file
    if not (file.startswith("3-")): #If the file does not start with the proper stage number
        continue #Skip it
    input = open(file, "r") #Open the file
    output = open(file.replace("3-","4-"), "w") #Create and open the output file

    output.write(input.readline()) #Copy the columns
        
    for line in input: #For each line in the input file
        dat = line.split(",") #Split line by commas
        latInFeet = coordOffset(float(dat[2])) #Convert coordinate latitude to feet
        longInFeet = coordOffset(float(dat[3])) #Convert coodinate longitude to feet
        output.write("{},{},{},{},{}".format(dat[0],dat[1],latInFeet,longInFeet,dat[4])) #Record converted data