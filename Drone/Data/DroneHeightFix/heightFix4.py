#This file calculates the height of the drone based on the speed at which it was moving. This is zSpeed
file = open("airData.csv", "r")
out = open("airDataFixed4.csv", "w")

items = file.readline().split(",")
items.insert(len(items)-1,"adjusted_height_feet")
out.write("{}\n".format(",".join(items)))

curHeight = 0;
lastTime = 0;
lastSpeed = 0;
lastSpeedFromPos = 0;

#print(items[len(items) - 2])

#print(items[20])
for line in file:
    data = line.split(",")
    if (data[0] == "0"): 
        curHeight = 0
        lastTime = 0
        
    if (data[20] == "0"): #If there is no speed
        curHeight = curHeight
    else: #If there is speed
        if (data[28] == "1024"): #If no throttle but there is speed
            curHeight = curHeight
        else: #If  speed and throttle
            timeDiff = (int(data[0]) - lastTime) / 1000 #in seconds
            speed = float(data[20]) * 1.1
            curHeight -= speed * timeDiff
    #print("curHeight: {} + {} += {}".format(timeDiff, data[20], curHeight))
    lastTime = int(data[0])
    lastSpeed = float(data[20])
    data.insert(len(data)-1,str(curHeight))
    out.write("{}".format(",".join(data)))