import sys
import os

args = sys.argv; #Gather args from command line

if not (len(args) == 3): #If there isn't 3 args
    print("USAGE: PosFix.py <LATITUDE> <LONGITUDE>") #print usage
    sys.exit(0) #Exit
    
#Set the necessary global variables
lat = 0
long = 0
dataFile = None
outputFile = None

try: #Starting a try block to test the following actions
    lat = float(args[1]) #Ensure given latitude value is a float (i.e., has a decimal and numbers following, even if just 0.)
    long = float(args[2]) #Ensure given longitude value is a float
except:
    print("Invalid parameter")
    sys.exit(0) #Exit if the try block catches an error.

filesInDir = os.listdir()
for file in filesInDir:
    if not (file.startswith("2-")):
        continue
    dataFile = open(file, "r")
    outputFile = open(file.replace("2-","3-"),"w")
    dataFile.readline() #Ignore column names


    outputFile.write("Time,RSSI,RelativeLatitude,RelativeLongitude,Height\n") #Add the column titles at the top

    for line in dataFile: #Iterate through every line in data file.
        data = line.split(",") #Split by comma (CSV file)
        relLat = ""
        relLong = ""
        try:
            relLat = float(data[2]) - lat #calculate relative latitude
            relLong = float(data[3]) - long #calculate relative longitude
            outputFile.write("{},{},{},{},{}".format(data[0], data[1], relLat, relLong, data[4])) #Write to output file.
        
        except:
            relLat = relLat #Just need a line here
        
    outputFile.close() #Close output file to write the bitstream
    