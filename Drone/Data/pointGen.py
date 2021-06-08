import sys


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
        
        #print("A")
        for i in range(curLocY+step, (N_len+1)*step, step): #N loop
            curLocY = i
            #print("{} or {} or {} or {} = {}".format((curLocX > maxX), (curLocX < minX), (curLocY > maxY), (curLocY < minY), checkBounds()))
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out == True):
                #print("A: {} > {} or {} < {} or {} > {} or {} < {} = {}".format(curLocX, maxX, curLocX , minX, curLocY , maxY, curLocY, minY, checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)))
                out = True
                break
            #print("A: {}, {}".format(curLocX, curLocY))
            iter += 1
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY))
        #print("B")
        for i in range(curLocX+step, (E_len+1)*step, step): #E loop
            curLocX = i
            #print("{} or {} or {} or {} = {}".format((curLocX > maxX), (curLocX < minX), (curLocY > maxY), (curLocY < minY), checkBounds()))
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)):
                #print("B: {} > {} or {} < {} or {} > {} or {} < {} = {}".format(curLocX, maxX, curLocX , minX, curLocY , maxY, curLocY, minY, checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)))
                out = True
                break
            #print("B: {}, {}".format(curLocX, curLocY))
            iter += 1
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY))
        #print("C")
        for i in range(curLocY-step, (S_len)*step, -1*step): #S_loop
            curLocY = i
            #print("C-pre: {} or {} or {} or {} = {}".format((curLocX > maxX), (curLocX < minX), (curLocY > maxY), (curLocY < minY), checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)))
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out):
                #print("C: {} > {} or {} < {} or {} > {} or {} < {} = {}".format(curLocX, maxX, curLocX , minX, curLocY , maxY, curLocY, minY, checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)))
                out = True
                break
            #print("C: {}, {}".format(curLocX, curLocY))
            iter += 1
            file.write("{},{},{},{}\n".format(iter, height, curLocX, curLocY))
        #print("D")
        for i in range(curLocX-step, (W_len)*step, -1*step): #S_loop
            curLocX = i
            #print("D-pre: {} or {} or {} or {} = {}".format((curLocX > maxX), (curLocX < minX), (curLocY > maxY), (curLocY < minY), checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)))
            if (checkBounds(curLocX, curLocY, minX, maxX, minY, maxY) or out):
                #print("D: {} > {} or {} < {} or {} > {} or {} < {} = {}".format(curLocX, maxX, curLocX , minX, curLocY , maxY, curLocY, minY, checkBounds(curLocX, curLocY, minX, maxX, minY, maxY)))
                out = True
                break
            #print("D: {}, {}".format(curLocX, curLocY))
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
    
    
#calcTimes(-100, 100, -100, 100, 3, 30, 20, 3, 5)
#print("*"*50)
#calcTimes(-100, 100, -100, 100, 3, 30, 10, 3, 5)
#print("*"*50)
#calcTimes(-100, 100, -100, 100, 3, 30, 5, 3, 5)
#print("*"*50)
#calcTimes(-100, 100, -100, 100, 3, 30, 1, 3, 5)
genCoordFile(-100, 100, -100, 100, 3, 30, 10, 3, "test.csv")