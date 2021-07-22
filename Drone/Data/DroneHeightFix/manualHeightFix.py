import os
filesInDir = os.listdir()
for fileName in filesInDir:
    if not fileName.startswith("0-"):
        continue
    newFileName = fileName.replace("0-","1-")
    file = open(fileName, "r")
    out = open(newFileName, "w")

    items = file.readline().split(",")
    items.insert(len(items)-1,"adjusted_height_feet")
    out.write("{}".format(",".join(items)))

    height = fileName.split(".")[0].split("-")[2].replace("foot","")

    for line in file:
        data = line.split(",")
        
        data.insert(len(data)-1,str(height))
        out.write("{}".format(",".join(data)))
