#Sets height based on file name

import os


filesInDir = os.listdir() #list of all files in directory
for fileName in filesInDir: #For all files in directory
    if not fileName.startswith("0-"): #If the file does not start with the proper stage number
        continue #Skip it
    newFileName = fileName.replace("0-","1-") #Create the new file name
    file = open(fileName, "r") #Open input file
    out = open(newFileName, "w") #Open output file

    items = file.readline().split(",") #Read line with column names and split by commas
    items.insert(len(items)-1,"adjusted_height_feet") #Insert a column before the last column
    out.write("{}".format(",".join(items))) #Join the array of column names and write to an output file

    height = fileName.split(".")[0].split("-")[2].replace("foot","") #Get the height value from the input file name

    for line in file: #For all lines in the input file
        data = line.split(",") #Split the line by commas
        
        data.insert(len(data)-1,str(height)) #Insert the height value in the proper column
        out.write("{}".format(",".join(data))) #Join the data together and write to a file
