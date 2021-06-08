import sys
import os

args = sys.argv; #Gather args from command line

if not (len(args) == 4 or len(args) == 5): #If there aren't 4 args or 5 args
    print("USAGE: PosFix.py <LATITUDE> <LONGITUDE> <INPUT FILE> [OUTPUT FILE]") #print usage
    sys.exit(0) #Exit
    
#Set the necessary global variables
lat = 0
long = 0
dataFile = None
outputFile = None

try: #Starting a try block to test the following actions
    lat = float(args[1]) #Ensure given latitude value is a float (i.e., has a decimal and numbers following, even if just 0.)
    long = float(args[2]) #Ensure given longitude value is a float
    dataFile = open(args[3], "r") #Open the input file, will trigger the except block if file doesn't exist
    outputFile = open(args[4] if len(args) == 5 else "output.csv", "w") #If an output file was supplied, open it. Otherwise open output.csv
except:
    print("Invalid parameter")
    sys.exit(0) #Exit if the try block catches an error.
    
dataFile.readline() #Ignore column names

if (os.stat(args[4] if len(args) == 5 else "output.csv").st_size == 0): #If the output file is empty (newly created)
    outputFile.write("Time,RSSI,RelativeLatitude,RelativeLongitude,Height\n") #Add the column titles at the top

for line in dataFile: #Iterate through every line in data file.
    data = line.split(",") #Split by comma (CSV file)
    relLat = float(data[2]) - lat #calculate relative latitude
    relLong = float(data[3]) - long #calculate relative longitude
    outputFile.write("{},{},{},{},{}".format(data[0], data[1], relLat, relLong, data[4])) #Write to output file.
    
outputFile.close() #Close output file to write the bitstream
    