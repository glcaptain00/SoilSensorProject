#This file calculates the height of the drone based on the speed at which it was moving and the throttle. Averages height of all points from last movement to create a flat layer
file = open("airData.csv", "r")
out = open("airDataFixed3.csv", "w")

items = file.readline().split(",")
items.insert(len(items)-1,"adjusted_height_feet")
out.write("{}\n".format(",".join(items)))

curHeight = 0;
lastTime = 0;

points = []
total = 0.0
iter = 0

#print(items[len(items) - 2])

#print(items[20])
for line in file:
    data = line.split(",")
    if (data[0] == "0" and not iter == 0): 
        avg = total / iter
        for item in points:
            item.insert(len(item)-1,str(avg))
            out.write(",".join(item))
        points = []
        iter = 0
        total = 0.0
        
    if (data[20] == "0" or data[28] == "1024"): #If there is no throttle
        points.append(data)
        total += float(data[4])
        iter += 1
    elif (not iter == 0):
        avg = total / iter
        for item in points:
            item.insert(len(item)-1,str(avg))
            out.write(",".join(item))
        points = []
        iter = 0
        total = 0.0
        
   