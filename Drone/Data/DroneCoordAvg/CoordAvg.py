import sys


outdat = {}
input = open(sys.argv[1], "r")
output = open(sys.argv[2], "w")
output.write("RSSI,Latitude,Longitude,Height\n")
input.readline()

def avg(table):
    sum = 0.0
    for i in range(len(table)):
        sum += table[i];
        
    return sum/len(table)
    
    
    
for line in input:
    data = line.split(",")
    key = "{},{},{}".format(data[2], data[3], data[4])
    if not key in outdat:
        outdat[key] = {}
        outdat[key]["RSSI"] = []
    else:
        print("DUPE")
    outdat[key]["RSSI"].append(float(data[1]))
    outdat[key]["AVG"] = avg(outdat[key]["RSSI"])
    
input.close()

for keys in outdat:
    output.write("{},{}".format(outdat[keys]["AVG"], keys));
        
output.close()
        