#####################################################################
# This code syncs data between Sensor and Drone via timestamps      #
# To determine the appropriate timestamp, estimated millisecond     #
# times are added to the drone's timestamps, and the sensor's       #
# times are rounded to the nearest tenth of a second. If the        #
# sensor's time does not have a matching drone time, then a         #
# time is selected by calculating the nearest recorded millisecond. #
#                                                                   #
# Any questions, contact Levi Captain at george.captain@okstate.edu #
#####################################################################




import json
import os

#Open the two files
drone = open("droneDat.csv", "r")
sensor = open("sensorDat.csv", "r")

#Read the top line. Top line contains column titles, so ignore this
drone.readline()
sensor.readline()

##SETUP FIRST LOOP
droneData = drone.readline() #Read the first line of data
prev_second = -1 #Set the previous second for time tracking
milli = 0 #Set the millisecond to 0 for time tracking
droneDataJSON = {} #Create a JavaScript Object Notation (JSON) object for storing the data. Allows parsing via keys.
##FINISH FIRST LOOP SETUP

##droneDataJSON format
#   droneDataJSON = {
#                       timestamp (accurate to seconds): {
#                                                           milli: {lat: x, long: y, height: z},
#                                                           milli: {lat: x, long: y, height: z},
#                                                           ...
#                                                        },
#                       timestamp (accurate to seconds): {
#                                                           milli: {lat: x, long: y, height: z},
#                                                           milli: {lat: x, long: y, height: z},
#                                                           ...
#                                                        },
#                       ...
#                   }
##end format

##FIRST LOOP
for data in drone: #For every line in the drone data file
    dDat = data.split(",") #split each line by ',' (Comma Seperated Value file)
    if (prev_second != int(dDat[1][17:19])): #If the previous second does not match the second of the current data file.   
        prev_second = int(dDat[1][17:19]) #Set the previous second to the current second
        milli = 0 #Reset milli to 0
    else:      
        milli += 1 #increase milli by 1 if not a new second
    
    if (milli == 0): #If a new second has occured
        droneDataJSON[dDat[1]] = {} #Create a new table for the new second
        
    droneDataJSON[dDat[1]][milli] = {} #Add a table within the timestamp's table for the millisecond data
    #Add lat, long, and height data to the milli table
    droneDataJSON[dDat[1]][milli]["lat"] = dDat[2]
    droneDataJSON[dDat[1]][milli]["long"] = dDat[3]
    droneDataJSON[dDat[1]][milli]["height"] = dDat[5]

drone.close() #Close the drone file.

#Name and open the output file
outFileName = "outfile.csv"
outputFile = open(outFileName, "a")

if (os.stat(outFileName).st_size == 0): #If the output file is empty (newly created)
    outputFile.write("Time,RSSI,Latitude,Longitude, Height above ground at drone location\n") #Add the column titles at the top


for data in sensor:  #For every line in the sensor data file
    sDat = data.split(",") #split each line by ',' (Comma Seperated Value file)
    
    ##Could probably be simplified some. '...' represents the result from the previous step. Steps:
    #1) sDat[0] -> Get timestamp
    #2) ...[19:26] -> Get the milliseconds, including the decimal (.)
    #3) float(...) -> Convert the acquired string into a float
    #4) round(...,1) -> Round the newly converted float to tenths place (1 place after decimal)
    #5) ... * 10 -> Multiply the result of round by 10 to move the digits left
    #6) int(...) -> Convert to integer
    mil = int(round(float(sDat[0][19:26]), 1) * 10)
    
    key = sDat[0].split(".")[0] #The timestamp is the key we search for in the outermost table.
    if (droneDataJSON.get(key) is None): #If the outermost table doesn't have a key associated with that timestamp
        outputFile.write("{},{},{},{},{}\n".format(sDat[0],sDat[1],"","","")) #Write a line with empty data.
        continue #continue to next iteration of loop to avoid writing another line of data.
    #If the timestamp value was found, but the millisecond value was not
    elif (droneDataJSON[key].get(mil) is None):
        latestMilli = 0 #Create var for tracking the most recent millisecond
        for tKey in dict.keys(droneDataJSON[key]): #loop through each key in the droneDataJSON[timestamp] table (i.e. the milliseconds)
            latestMilli = latestMilli if (int(tKey) < latestMilli) else int(tKey) #If the current key is more recent then the stored latest, then change it.

        nextSecondTimestamp = "{}{:0>2d}".format(key[0:17], int(key[17:19]) + 1) #Create the next timestamp string
        
        #Calculate differences between previous time and next time
        diffPrev = mil - latestMilli
        diffNext = 10 - mil
        
        if (diffPrev < diffNext or droneDataJSON.get(nextSecondTimestamp) is None): #If current - prev < next - current OR if the next second doesn't exist
            mil = latestMilli #Set mil to the latest mil
        else:
            key = nextSecondTimestamp #Update key to new timestamp
            mil = 0 #Fix mil according to new timestamp


    syncDat = droneDataJSON[key][mil] #Get the data from the JSON object
    outputFile.write("{},{},{},{},{}\n".format(sDat[0],sDat[1],syncDat["lat"],syncDat["long"],syncDat["height"])) #Write the data to the output file
       
outputFile.close() #Close output file when finished 
