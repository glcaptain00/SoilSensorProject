import sys
import pykml
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

def checkBounds(curLocX, curLocY, minX, maxX, minY, maxY):
    return (curLocX > maxX) or (curLocX < minX) or (curLocY > maxY) or (curLocY < minY)

def genCoordFile(minX, maxX, minY, maxY, minH, maxH, step, stepH, file_name):
    file = open(file_name, "w")
    file.write("iter,height,Relative Latitude,Relative Longitude\n")

    N_len = 1
    E_len = 1
    S_len = -2
    W_len = -2

    iter = 0
    curLocX = 0
    curLocY = 0
    height = minH
    out = False
    file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY))
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
                file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY))
        
        for i in range(curLocY+step, (N_len+1)*step, step): #N loop
            curLocY = i
            
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out == True):
                out = True
                break
            iter += 1
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY))
        for i in range(curLocX+step, (E_len+1)*step, step): #E loop
            curLocX = i
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)):    
                out = True
                break
            iter += 1
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY))
        for i in range(curLocY-step, (S_len)*step, -1*step): #S_loop
            curLocY = i
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out):   
                out = True
                break
            iter += 1
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY))
        for i in range(curLocX-step, (W_len)*step, -1*step): #S_loop
            curLocX = i
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out):   
                out = True
                break
            iter += 1
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY))
        file.flush()
        N_len += 1;
        E_len += 1;
        S_len -= 1;
        W_len -= 1;

def calcTimes(minX, maxX, minY, maxY, minH, maxH, step, stepH, seconds_per_point):
    numLayers = int((maxH - minH)/stepH)+1
    numPointsPerLayer = (((maxX - minX) / step) + 1) * (((maxY - minY) / step) + 1)
    totTime = numPointsPerLayer * numLayers * seconds_per_point
    print("BOUNDS:\n\t{} <= x <= {}\n\t{} <= y <= {}\n\t{} <= h <= {}".format(minX, maxX, minY, maxY, minH, maxH))
    print("STEP SIZE:          {}".format(step))
    print("POINTS PER LAYER:   {}".format(numPointsPerLayer))
    print("NUMBER OF LAYERS:   {}".format(numLayers))
    print("TOTAL # OF POINTS:  {}".format(numPointsPerLayer * numLayers))
    print("SECONDS PER POINT: {}".format(seconds_per_point))
    print("="*50)
    print("Expected runtime:\t\t\t {} hours, {} minutes, {} seconds".format(int(totTime/60/60), int(totTime/60%60), int(totTime%60)))
    totTime *= 2
    print("Doubled for second polarization:\t {} hours, {} minutes, {} seconds".format(int(totTime/60/60), int(totTime/60%60), int(totTime%60)))
    
def genLitchiCoordFile(origX, origY, minX, maxX, minY, maxY, minH, maxH, step, stepH, file_name):
    file = open(file_name, "w")
    #file.write("Latitude,Longitude,Altitude (ft)\n")

    N_len = 1
    E_len = 1
    S_len = -2
    W_len = -2

    iter = 0
    curLocX = 0
    curLocY = 0
    height = minH
    out = False
    file.write("{},{},{}\n".format(curLocY + origY, curLocX + origX, height))
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




#calcTimes(-100, 100, -100, 100, 3, 30, 20, 3, 5)
#print("*"*50)
#calcTimes(-100, 100, -100, 100, 3, 30, 10, 3, 5)
#print("*"*50)
#calcTimes(-100, 100, -100, 100, 3, 30, 5, 3, 5)
#print("*"*50)
#calcTimes(-100, 100, -100, 100, 3, 30, 1, 3, 5)
#genCoordFile(-100, 100, -100, 100, 3, 30, 10, 3, "test.csv")
#genLitchiCoordFile(-97.066469, 36.125689, -0.0002, 0.0002, -0.0002, 0.0002, 1, 1, 0.00004, 1, "Litchi_coords.csv")
genKmlFile(-97.066469, 36.125689, 273, -0.0002, 0.0002, -0.0002, 0.0002, 1, 10, 0.00004, 1, "FlightPath.kml")

