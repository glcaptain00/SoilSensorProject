# Import Python System Libraries
import os
import time 
from time import sleep
from datetime import datetime


# Import Blinka Libraries
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
# Import the SSD1306 module.
import adafruit_ssd1306 as oled
# Import RFM9x
import adafruit_rfm9x as lora


##########################################################
# IF transmit packets immediately after receiving,
# Implement a timer for testing to verify this is
# feasable
##########################################################

#IF IMPLEMENTING QUEUE METHOD
#tx_queue = []

while (True): #Loop forever
    pack = None #Clear the previous packet (Or set to None if there is no previous packet.
    pack = lora.receive() #Receive the packet
    
    if (pack == None): #If no packet received
        print("No packet")
    else: #If packet received
        print("Packet: {}".format(pack))
        #FIXME: verify following bitmasking
        #ASSUMING PACKET IS HEX CODE SENT FROM TRANSMITTER
        #0x0 -> From sensor
        #0xF -> From relay
        pack = int(pack, 16)
        if (pack & 0xF != 0x0): #if packet came from sensor, then src bits = 0
            continue
        pack = pack | 0x1 # 0xXXXX XX...XX XXX? or 0x1 =  0xXXXX XX...XX XXX! where ? -> xxx0 and ! -> xxx1 (X = 4 bits, x = 1 bit)
        lora.send(str(pack)) #Retransmit packet
