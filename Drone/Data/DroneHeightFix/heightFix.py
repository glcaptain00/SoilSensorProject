#This file calculates the height of the drone based on the speed at which it was moving. This is zSpeed
file = open("airData.csv", "r")
out = open("airDataFixed.csv", "w")

items = file.readline().split(",")
items.insert(len(items)-1,"adjusted_height_feet")
out.write("{}\n".format(",".join(items)))

curHeight = 0;
lastTime = 0;

#print(items[len(items) - 2])

#print(items[20])
for line in file:
    data = line.split(",")
    if (data[0] == "0"):
        curHeight = 0
        lastTime = 0;
    timeDiff = (int(data[0]) - lastTime) / 1000 #Get's time difference in seconds
    curHeight -= timeDiff * (float(data[20]) * (5280 / (60 * 60)))
    #print("curHeight: {} + {} += {}".format(timeDiff, data[20], curHeight))
    lastTime = int(data[0])
    data.insert(len(data)-1,str(curHeight))
    out.write("{}".format(",".join(data)))