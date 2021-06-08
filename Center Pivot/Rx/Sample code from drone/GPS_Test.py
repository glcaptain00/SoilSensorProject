import os
import time
from datetime import datetime
import threading
import sys
import serial

testFile = open("/home/pi/gps_test.csv", "a")
gpsReader = serial.Serial('/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_7_-_GPS_GNSS_Receiver-if00',115200, timeout = 5)

if os.stat("/home/pi/gps_test.csv").st_size == 0: #From Fahim's code, if the file is empty, add the first line. 
        testFile.write("Time,Latitude,Longitude\n") #The first line here will be the proper format for column labels in a CSV file
        

for i in range(0,200): #arbitrary loop. Just getting data for 20 iterations
    line = gpsReader.readline().strip().decode('ascii')
    if (len(line) == 0):
        print("Timed out!")
        sys.exit(0)
    dat = line.split(',')
    while (dat[0] != "$GPGGA" and dat[0] != "$GPRMC"):
        #print("Waiting for $GPGGA or $GPRMC. \nLast message type: %s" % dat[0])
        line = gpsReader.readline().strip().decode('ascii')
        dat = line.split(',')
    #else:
        #print("%s message received. Continuing..." % dat[0])
        
    curTime = datetime.now() #Get the current time

    #print("%d" % i)
    #print("Fixed: %s" % dat[6])
    
    long = "%s" % (dat[4] if dat[0] == "$GPRMC" else "%s %s" % (dat[2], dat[3]))
    lat = "%s" % (dat[3] if dat[0] == "$GPRMC" else "%s %s" % (dat[2], dat[3]))

    toWrite = "%s,%s,%s\n" % (str(curTime), lat, long)
    print("toWrite: %s" % toWrite)
    testFile.write(toWrite) #write data to file

    #Not necessary. Serial waits on its own
    #time.sleep(0.1) #wait for 1 second

testFile.close()
print("Finished!")

