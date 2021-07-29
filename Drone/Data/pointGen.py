# This file has several different functions for generating the points for the drone to fly in several different formats.

import sys
import pykml
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

#This function generates a line with all the items in a litchi mission CSV file
def genLitchiLine(curLocX, curLocY, origX, origY, height, origH, pause, file):
    
    #This line gets split at the very end
    items = "latitude,longitude,altitude(ft),heading(deg),curvesize(ft),rotationdir,gimbalmode,gimbalpitchangle,actiontype1,actionparam1,actiontype2,actionparam2,actiontype3,actionparam3,actiontype4,actionparam4,actiontype5,actionparam5,actiontype6,actionparam6,actiontype7,actionparam7,actiontype8,actionparam8,actiontype9,actionparam9,actiontype10,actionparam10,actiontype11,actionparam11,actiontype12,actionparam12,actiontype13,actionparam13,actiontype14,actionparam14,actiontype15,actionparam15,altitudemode,speed(m/s),poi_latitude,poi_longitude,poi_altitude(ft),poi_altitudemode,photo_timeinterval,photo_distinterval".split(",")
    
    coordString = "" #Create a variable to store the string to return
    for j in range(len(items)): #For each of the items
        data = "" #Store a data value

        #Depending on the name of the item, a variety of values must be set.
        if (items[j].startswith("actiontype")):
            if (items[j] == "actiontype1"):
                data = "0"
            else:
                data = "-1"
        elif (items[j].startswith("actionparam")):
            if (items[j] == "actionparam1"):
                data = pause
            else:
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
            data = "0"
        elif (items[j].startswith("poi")):
            data = "0"
        elif (items[j].startswith("photo")):
            data = "-1"
        
        #Add data to coordString    
        coordString += "{}{}".format("" if (coordString == "") else ",", data)
    return coordString #return the generated litchi line

def checkBounds(curLocX, curLocY, minX, maxX, minY, maxY): #Checks to see if the current location is within the bounds
    return (curLocX > maxX) or (curLocX < minX) or (curLocY > maxY) or (curLocY < minY)

def genCoordFile(minX, maxX, minY, maxY, minH, maxH, step, stepH, file_name): #Generate a basic CSV file that contains the coordinates being collected.
    file = open(file_name, "w")
    file.write("iter,height,Relative Latitude,Relative Longitude\n")

    N_len = 1  #Initial number of steps North
    E_len = 1  #Initial number of steps East
    S_len = 2  #Initial number of steps South
    W_len = 2  #Initial number of steps West

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

def calcTimes(minX, maxX, minY, maxY, minH, maxH, step, stepH, seconds_per_point): #Calculate the general flight time of the drone.
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
    
def genLitchiCoordFile(origX, origY, origH, minX, maxX, minY, maxY, minH, maxH, step, stepH, pause, pointLim, file_name): #Generate a coordinate file for litchi
    flightIter = 1 #Iterator to keep track of the number of separate missions for litchi. Needed due to 99 point limit
    file = open("{}_flight{}.csv".format(file_name, flightIter), "w")
    #file.write("Latitude,Longitude,Altitude (ft)\n")

    N_len = 1  #Initial steps
    E_len = 1  #Initial steps
    S_len = 2 #Initial steps
    W_len = 2 #Initial steps
    
    iter = 0 #Iteration variable.
    curLocX = 0 #Initial position
    curLocY = 0 #Initial position
    height = minH #Initial Height
    out = False #Out of bounds tracker
    coordString = genLitchiLine(curLocX, curLocY, origX, origY, height, origH, pause, file)
    file.write("{}\n".format(coordString)) #Write down first line of new layer
    while (True): #Run forever, or until loop is broken
        if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out): #If outside of bounds
            height += stepH; #Increase height
            curLocX = 0 #Reset position
            curLocY = 0 #Reset position
            N_len = 1   #Reset steps
            E_len = 1   #Reset steps
            S_len = 2   #Reset steps
            W_len = 2   #Reset steps
            #iter = 0    #Reset iteration
            out = False #Reset out of bounds tracker
            if (height > maxH): #If the new height is greater than the max height
                break #Break the while loop
            else:
                coordString = genLitchiLine(curLocX, curLocY, origX, origY, height, origH, pause, file)
                file.write("{}\n".format(coordString)) #Write down first line of new layer
        
        for i in range(1, N_len + 1): #N loop
            if (iter >= pointLim): #If the number of points is greater than or equal to the point limit
                file.close() #Close the current file
                flightIter += 1 #Increase the flight iterator
                file = open("{}_flight{}.csv".format(file_name, flightIter), "w") #Open new file
                iter = 0 #Reset point iterator
            curLocY += step #Adjust current location Y to move via the loop
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out): #If out of bounds
                out = True #Set out of bounds tracker to True
                break #Break this for loop
            iter += 1 #Increase point iterator
            coordString = genLitchiLine(curLocX, curLocY, origX, origY, height, origH, pause, file)
            file.write("{}\n".format(coordString)) #Write coordinate to file
        for i in range(1, E_len + 1): #E loop
            if (iter >= pointLim): #If the number of points is greater than or equal to the point limit
                file.close() #Close the current file
                flightIter += 1 #Increase the flight iterator
                file = open("{}_flight{}.csv".format(file_name, flightIter), "w") #Open new file
                iter = 0 #Reset point iterator
            curLocX += step #Adjust current location X to move via the loop
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)): #If out of bounds    
                out = True #Set out of bounds tracker to True
                break #Break this for loop
            iter += 1 #Increase point iterator
            coordString = genLitchiLine(curLocX, curLocY, origX, origY, height, origH, pause, file)
            file.write("{}\n".format(coordString)) #Write coordinate to file
        for i in range(1, S_len + 1): #S_loop
            if (iter >= pointLim): #If the number of points is greater than or equal to the point limit
                file.close() #Close the current file
                flightIter += 1 #Increase the flight iterator
                file = open("{}_flight{}.csv".format(file_name, flightIter), "w") #Open new file
                iter = 0 #Reset point iterator
            curLocY -= step #Adjust current location Y to move via the loop
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out): #If out of bounds   
                out = True #Set out of bounds tracker to True
                break #Break this for loop
            iter += 1 #Increase point iterator
            coordString = genLitchiLine(curLocX, curLocY, origX, origY, height, origH, pause, file)
            file.write("{}\n".format(coordString)) #Write coordinate to file
        for i in range(1, W_len + 1): #W_loop
            if (iter >= pointLim): #If the number of points is greater than or equal to the point limit
                file.close() #Close the current file
                flightIter += 1 #Increase the flight iterator
                file = open("{}_flight{}.csv".format(file_name, flightIter), "w") #Open new file
                iter = 0 #Reset point iterator
            curLocX -= step #Adjust current location X to move via the loop
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out): #If out of bounds   
                out = True #Set out of bounds tracker to True
                break #Break this for loop
            iter += 1 #Increase point iterator
            coordString = genLitchiLine(curLocX, curLocY, origX, origY, height, origH, pause, file)
            file.write("{}\n".format(coordString)) #Write coordinate to file
        file.flush() #Flush file in case of program crash. This ensures that everything done so far gets recorded
        N_len += 2; #Adjust steps
        E_len += 2; #Adjust steps
        S_len += 2; #Adjust steps
        W_len += 2; #Adjust steps

def genLitchiPrelimFile(origX, origY, origH, minX, maxX, minY, maxY, minH, maxH, stepH, speed, pause, file_name):    
    file = open("{}.csv".format(file_name), "w")
    items = "latitude,longitude,altitude(ft),heading(deg),curvesize(ft),rotationdir,gimbalmode,gimbalpitchangle,actiontype1,actionparam1,actiontype2,actionparam2,actiontype3,actionparam3,actiontype4,actionparam4,actiontype5,actionparam5,actiontype6,actionparam6,actiontype7,actionparam7,actiontype8,actionparam8,actiontype9,actionparam9,actiontype10,actionparam10,actiontype11,actionparam11,actiontype12,actionparam12,actiontype13,actionparam13,actiontype14,actionparam14,actiontype15,actionparam15,altitudemode,speed(m/s),poi_latitude,poi_longitude,poi_altitude(ft),poi_altitudemode,photo_timeinterval,photo_distinterval".split(",")
    curLocX = 0
    curLocY = 0
    positions = [[0,0], [0,minY], [0,maxY], [0,0], [minX,0], [maxX, 0]]
    height = minH
    for i in range(0, (int)((maxH - minH)/stepH) + 1):
        for pos in positions:
            [curLocX, curLocY] = pos
            coordString = genLitchiLine(curLocX, curLocY, origX, origY, height, origH, pause, file)
            file.write("{}\n".format(coordString))
            file.flush()
        height += stepH
    file.close()





#Coordinates of soil sensor:
# -97.083522
# 36.131149

### THESE LINES ARE TEST FLIGHTS AT THE OSU USRI BUILDING. NOT AT THE AIR FIELD
#Fewer Points
#genLitchiCoordFile(-97.083522, 36.131149, 0, -0.0002, 0.0002, -0.0002, 0.0002, 1, 5, 0.00005, 1, 5000, 45, "Litchi_coords")
#Less Dense
#genLitchiCoordFile(-97.083522, 36.131149, 0, -0.0002, 0.0002, -0.0002, 0.0002, 1, 5, 0.0001, 1, 5000, 90, "Litchi_coords")



#AIR FIELD
#genLitchiCoordFile(-96.835393, 36.162516, 0, -0.0002, 0.0002, -0.0002, 0.0002, 1, 5, 0.00005, 1, 5000, "Litchi_coords")