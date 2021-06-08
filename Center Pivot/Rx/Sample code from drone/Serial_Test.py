import os, sys
import serial
import time

ser = serial.Serial('/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_7_-_GPS_GNSS_Receiver-if00',19200, timeout = 5)

# listen for the input, exit if nothing received in timeout period
while True:
   line = ser.readline().strip().decode('ascii')
   if len(line) == 0:
      print("Time out! Exit.\n")
      sys.exit()
   dat = line.split(",")
   
   
   if (dat[0] == '$GPGGA'):
	   print("Time, position, and fix related data")
	   print("UTC of position fix: %s" % str(dat[1]))
	   print("Latitude: %s %s" % (str(dat[2]), str(dat[3])))
	   print("Longitude: %s %s" % (str(dat[4]), str(dat[5])))
   else:
       print("Command not implemented: %s" % dat[0])
   
