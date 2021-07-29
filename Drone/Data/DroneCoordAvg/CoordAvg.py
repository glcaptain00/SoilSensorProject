#Do not use this code :)
#Has not been updated, and is generally unnecessary.
#Initially intended to average values that were all at the same point because MATLAB would just remove the old values and only show the new ones.

import sys

outdat = {} #Create dict for output data
input = open(sys.argv[1], "r") #Open input file
output = open(sys.argv[2], "w") #Open output file
output.write("RSSI,Latitude,Longitude,Height\n") #Write column headers
input.readline() #Read the column headers from the input file.

def avg(table): #Define a function to calculate the average from a given table
    sum = 0.0 #Create a sum variable
    for i in range(len(table)): #Loop through all the values in the table
        sum += table[i] #Add the values of table to the sum
        
    return sum/len(table) #return sum over number of values
    
    
    
for line in input: #For all lines in the input file
    data = line.split(",") #Split the line by commas
    key = "{},{},{}".format(data[2], data[3], data[4]) #Create a key for the dict using the coordinates
    if not key in outdat: #If the coordinate key does not already exist
        outdat[key] = {} #Create an empty entry for the key
        outdat[key]["RSSI"] = [] #Create an array for the RSSI values
    #else: #If the coordinate key already exists
        #print("DUPE") #Debug message
    outdat[key]["RSSI"].append(float(data[1])) #Add the RSSI value of the current line
    outdat[key]["AVG"] = avg(outdat[key]["RSSI"]) #Calcuate the new average. This could have been done more efficiently by doing it once at the end
    
input.close() #close the input file

for keys in outdat: #For all the coordinate keys in output data
    output.write("{},{}".format(outdat[keys]["AVG"], keys)) #Write the data to a file
        
output.close() #Close the output, flushing the stream.
        