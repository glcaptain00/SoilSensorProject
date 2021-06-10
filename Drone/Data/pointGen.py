import sys
import pykml
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

def checkBounds(curLocX, curLocY, minX, maxX, minY, maxY): #Checks to see if the current location is within the bounds
    return (curLocX > maxX) or (curLocX < minX) or (curLocY > maxY) or (curLocY < minY)

def genCoordFile(minX, maxX, minY, maxY, minH, maxH, step, stepH, file_name): #Generate a basic CSV file that contains the coordinates being collected.
    file = open(file_name, "w")
    file.write("iter,height,Relative Latitude,Relative Longitude\n")

    N_len = 1  #Initial number of steps North
    E_len = 1  #Initial number of steps East
    S_len = -2 #Initial number of steps South
    W_len = -2 #Initial number of steps West

    iter = 0 #Iteration variable. Used to keep track of total points.
    curLocX = 0 #Initalize Current position to 0 (the origin)
    curLocY = 0 #Initalize Current position to 0 (the origin)
    height = minH #Initialize current height to the minimun height
    out = False #Track if drone is out of bounds.
    file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY)) #Write first coordinate
    while (True): #Run forever, or until loop is broken
        if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out): #If outside of bounds
            height += stepH; #Increase height
            curLocX = 0 #Reset position
            curLocY = 0 #Reset position
            N_len = 1   #Reset steps
            E_len = 1   #Reset steps
            S_len = -2  #Reset steps
            W_len = -2  #Reset steps
            iter = 0    #Reset iteration
            out = False #Reset out of bounds tracker
            if (height > maxH): #If the new height is greater than the max height
                break #Break the while loop
            else:
                file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY)) #Write down first coordinate of new layer
        
        for i in range(curLocY+step, (N_len+1)*step, step): #N loop
            curLocY = i #Adjust current location Y to move via the loop
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out): #If out of bounds
                out = True #Set out of bounds tracker to True
                break #Break this for loop
            iter += 1 #increase iteration counter
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY)) #Write coordinate to file
        for i in range(curLocX+step, (E_len+1)*step, step): #E loop
            curLocX = i #Adjust current location X to move via the loop
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)): #If out of bounds    
                out = True #Set out of bounds tracker to True
                break #Break this for loop
            iter += 1 #increase iteration counter
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY)) #Write coordinate to file
        for i in range(curLocY-step, (S_len)*step, -1*step): #S_loop
            curLocY = i #Adjust current location Y to move via the loop
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out): #If out of bounds   
                out = True #Set out of bounds tracker to True
                break #Break this for loop
            iter += 1 #increase iteration counter
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY)) #Write coordinate to file
        for i in range(curLocX-step, (W_len)*step, -1*step): #S_loop
            curLocX = i #Adjust current location X to move via the loop
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out): #If out of bounds   
                out = True #Set out of bounds tracker to True
                break #Break this for loop
            iter += 1 #increase iteration counter
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY)) #Write coordinate to file
        file.flush() #Flush file in case of program crash. This ensures that everything done so far gets recorded
        N_len += 1; #Adjust steps
        E_len += 1; #Adjust steps
        S_len -= 1; #Adjust steps
        W_len -= 1; #Adjust steps

def calcTimes(minX, maxX, minY, maxY, minH, maxH, step, stepH, seconds_per_point):
    numLayers = int((maxH - minH)/stepH)+1 #Calculate the number of layers
    numPointsPerLayer = (((maxX - minX) / step) + 1) * (((maxY - minY) / step) + 1) #Calculate the number of points per layer
    totTime = numPointsPerLayer * numLayers * seconds_per_point #Calculate total time from number of layers, number of points per layer, and number of seconds per point
    print("BOUNDS:\n\t{} <= x <= {}\n\t{} <= y <= {}\n\t{} <= h <= {}".format(minX, maxX, minY, maxY, minH, maxH)) #Printing the info to the console.
    print("STEP SIZE:          {}".format(step)) #Printing the info to the console.
    print("POINTS PER LAYER:   {}".format(numPointsPerLayer)) #Printing the info to the console.
    print("NUMBER OF LAYERS:   {}".format(numLayers)) #Printing the info to the console.
    print("TOTAL # OF POINTS:  {}".format(numPointsPerLayer * numLayers)) #Printing the info to the console.
    print("SECONDS PER POINT: {}".format(seconds_per_point)) #Printing the info to the console.
    print("="*50) #Used as a seperator.
    print("Expected runtime:\t\t\t {} hours, {} minutes, {} seconds".format(int(totTime/60/60), int(totTime/60%60), int(totTime%60))) #Display total time
    totTime *= 2 #Multiply by two for two iterations of flight. (i.e. Parallel and Skew antenna orientations.)
    print("Doubled for second polarization:\t {} hours, {} minutes, {} seconds".format(int(totTime/60/60), int(totTime/60%60), int(totTime%60))) #Display total time for 2 iterations (i.e. Parallel and Skew antenna orientations.)
    
def genLitchiCoordFile(origX, origY, minX, maxX, minY, maxY, minH, maxH, step, stepH, file_name):
    file = open(file_name, "w")
    #file.write("Latitude,Longitude,Altitude (ft)\n")

    N_len = 1  #Initial steps
    E_len = 1  #Initial steps
    S_len = -2 #Initial steps
    W_len = -2 #Initial steps

    iter = 0 #Iteration variable.
    curLocX = 0 #Initial position
    curLocY = 0 #Initial position
    height = minH #Initial Height
    out = False #Out of bounds tracker
    file.write("{},{},{}\n".format(curLocY + origY, curLocX + origX, height)) #Write initial coordinate.
    while (True):
        if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out):
            height += stepH;
            curLocX = 0
            curLocY = 0
            N_len = 1
            E_len = 1
            S_len = -2
            W_len = -2
            iter = 0
            out = False
            if (height > maxH):
                break
            else:
                file.write("{},{},{}\n".format(curLocY + origY, curLocX + origX, height))
        
        curLocY += N_len * step
        if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)):
                continue
        file.write("{},{},{}\n".format(curLocY + origY, curLocX + origX, height))
        curLocX += E_len * step
        if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)):
                continue
        file.write("{},{},{}\n".format(curLocY + origY, curLocX + origX, height))
        curLocY += S_len*step
        if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)):
                continue
        file.write("{},{},{}\n".format(curLocY + origY, curLocX + origX, height))
        curLocX += W_len * step
        if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)):
                continue
        file.write("{},{},{}\n".format(curLocY + origY, curLocX + origX, height))
        file.flush()
        
        N_len += 2;
        E_len += 2;
        S_len -= 2;
        W_len -= 2;

def genKmlFile(origX, origY, origH, minX, maxX, minY, maxY, minH, maxH, step, stepH, file_name):
    file = open(file_name, "w")
    kmlData = KML.Folder(KML.name('Folder'))
    kmlLine = KML.LineString(
        KML.altitudeMode('absolute')
    )
    kmlPlacemark = KML.Placemark(KML.name('Flight path'), kmlLine)
    kmlData.append(kmlPlacemark)

    N_len = 1
    E_len = 1
    S_len = 2
    W_len = 2

    iter = 0
    curLocX = 0
    curLocY = 0
    height = minH
    out = False
    coordinateString = "{},{},{}".format(curLocX + origX, curLocY + origY, height + origH)
    while (True):
        if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out):
            height += stepH;
            curLocX = 0
            curLocY = 0
            N_len = 1
            E_len = 1
            S_len = 2
            W_len = 2
            iter = 0
            out = False
            if (height > maxH):
                break
            else:
                coordinateString += " {},{},{}".format(curLocX + origX, curLocY + origY, height + origH)
        
        for i in range(1, N_len + 1): #N loop
            curLocY += step
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out == True):
                out = True
                break
            iter += 1
            coordinateString += " {},{},{}".format(curLocX + origX, curLocY + origY, height + origH)
        for i in range(1, E_len + 1): #E loop
            curLocX += step
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)):
                out = True
                break
            iter += 1
            coordinateString += " {},{},{}".format(curLocX + origX, curLocY + origY, height + origH)
        for i in range(1, S_len + 1): #S_loop
            curLocY -= step
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out):
                out = True
                break
            iter += 1
            coordinateString += " {},{},{}".format(curLocX + origX, curLocY + origY, height + origH)
        for i in range(1, W_len+1): #W_loop
            curLocX -= step        
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out):
                out = True
                break
            iter += 1
            coordinateString += " {},{},{}".format(curLocX + origX, curLocY + origY, height + origH)
        
        
        N_len += 2;
        E_len += 2;
        S_len += 2;
        W_len += 2;

    kmlLine.append(KML.coordinates(coordinateString))
    file.write(etree.tostring(kmlData, pretty_print=True, encoding='unicode'))

def genLitchiPrelimFile(origX, origY, origH, minX, maxX, minY, maxY, minH, maxH, stepH, speed, file_name):    
    file = open(file_name, "w")
    items = "latitude,longitude,altitude(ft),heading(deg),curvesize(ft),rotationdir,gimbalmode,gimbalpitchangle,actiontype1,actionparam1,actiontype2,actionparam2,actiontype3,actionparam3,actiontype4,actionparam4,actiontype5,actionparam5,actiontype6,actionparam6,actiontype7,actionparam7,actiontype8,actionparam8,actiontype9,actionparam9,actiontype10,actionparam10,actiontype11,actionparam11,actiontype12,actionparam12,actiontype13,actionparam13,actiontype14,actionparam14,actiontype15,actionparam15,altitudemode,speed(m/s),poi_latitude,poi_longitude,poi_altitude(ft),poi_altitudemode,photo_timeinterval,photo_distinterval".split(",")
    curLocX = 0
    curLocY = 0
    positions = [[0,0], [0,minY], [0,maxY], [0,0], [minX,0], [maxX, 0]]
    height = minH
    for i in range(0, (int)((maxH - minH)/stepH) + 1):
        for pos in positions:
            coordString = ""
            [curLocX, curLocY] = pos
            for j in range(len(items)):
                data = ""
                if (items[j].startswith("actiontype")):
                    data = "-1"
                elif (items[j].startswith("actionparam")):
                    data = "0"
                elif (items[j].startswith("curvesize")):
                    data = "NaN"
                elif (items[j].startswith("rotation")):
                    data = "0"
                elif (items[j].startswith("gimbal")):
                    data = "0"
                elif (items[j].startswith("latitude")):
                    data = curLocY + origY
                elif (items[j].startswith("longitude")):
                    data = curLocX + origX
                elif (items[j].startswith("altitude(")):
                    data = height + origH
                elif (items[j].startswith("heading")):
                    data = "0"
                elif (items[j].startswith("altitudemode")):
                    data = "1"
                elif (items[j].startswith("speed")):
                    data = speed
                elif (items[j].startswith("poi")):
                    data = "0"
                elif (items[j].startswith("photo")):
                    data = "-1"
                coordString += "{}{}".format("" if (coordString == "") else ",", data)
            file.write("{}\n".format(coordString))
            file.flush()
        height += stepH
    file.close()






#calcTimes(-100, 100, -100, 100, 3, 30, 20, 3, 5)
#print("*"*50)
#calcTimes(-100, 100, -100, 100, 3, 30, 10, 3, 5)
#print("*"*50)
#calcTimes(-100, 100, -100, 100, 3, 30, 5, 3, 5)
#print("*"*50)
#calcTimes(-100, 100, -100, 100, 3, 30, 1, 3, 5)
#genCoordFile(-100, 100, -100, 100, 3, 30, 10, 3, "test.csv")
#genLitchiCoordFile(-97.066469, 36.125689, -0.0002, 0.0002, -0.0002, 0.0002, 1, 1, 0.00004, 1, "Litchi_coords.csv")
genLitchiPrelimFile(-97.066469, 36.125689, 0,  -0.0002, 0.0002, -0.0002, 0.0002, 3, 10, 1, 1.5, "Litchi_prelim.csv")
#genKmlFile(-97.066469, 36.125689, 273, -0.0002, 0.0002, -0.0002, 0.0002, 1, 10, 0.00004, 1, "FlightPath.kml")

