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
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x

# Button A
btnA = DigitalInOut(board.D5)
btnA.direction = Direction.INPUT
btnA.pull = Pull.UP

# Button B
btnB = DigitalInOut(board.D6)
btnB.direction = Direction.INPUT
btnB.pull = Pull.UP

# Button C
btnC = DigitalInOut(board.D12)
btnC.direction = Direction.INPUT
btnC.pull = Pull.UP

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
rfm9x.tx_power = 5
rfm9x.enable_crc = True
rfm9x.node = 0xFE
prev_packet = None

#Function to convert 16 bit hex value to signed decimal
def hex16toSInt(val):
    return -(val & 0x8000) | (val & 0x7fff) #First part determines the sign. The MSB is either 1 or 0. If it is 1, then you have -1 * 1, which means the sign carries over. The second part calculated the value of the rest of the bits

start = time.time()

#Time to run
PERIOD_OF_TIME = 20

#Packet receive config
PACKET_TIMEOUT = 5 #seconds
PACKET_WITH_HEADER = True #Whether or not to collect the header bytes with the packet

#Log file config
logDir = "/home/pi" #Directory to place log file
filename = "data_log.csv" #Name of log file

file = open("{}/{}".format(logDir, filename), "a") #Open log file based on previous configuration
i=0
if os.stat("/home/pi/data_log.csv").st_size == 0: #if the the file has just been created
        file.write("Time,UUID,Soil Moisture,RSSI (Sensor to Relay),RSSI (Relay to Base),Raw Packet\n") #Write the column names


no_packet_start_time = time.time() #Log the start time. For packet loss purposes.

while True:
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)

    # check for packet rx
    packet = rfm9x.receive(timeout=PACKET_TIMEOUT, with_header=PACKET_WITH_HEADER)
    if (packet is None):
        if (time.time() >= no_packet_start_time + 5):
            display.show()
            display.text('- PKT LOSS -', 35, 20, 1)
            print("Packet loss")
            file.write("{},{}\n".format(datetime.now(), "Packet Loss"))
            no_packet_start_time = time.time()
    else:
        #print('PACKET RECEIVED: {}'.format(datetime.now()))
        data = packet #.split("\\x")
        # Display the packet text and rssi
        display.fill(0)
        #This assumes the packet remains in 1 hex string in place of the multiple bytes       
        rawpacket = "0x" #String for storing raw packet
        for item in data:
            rawpacket += '{:02X}'.format(item)

        #The following lines handle the bitmasking. If PACKET_WITH_HEADER is true, then the packets will be requested with headers and these masks will not break. 
        #These lines use ternary operators to achieve this. Ternary operators: (value1 if condition else value2)
        id = data[0 + (4 if (PACKET_WITH_HEADER) else 0)] >> 2  #Not really necessary anymore. RadioHead library sends a 4 byte header that includes a "From" byte. This byte will contain the id
        sensorRSSI = (data[2 + (4 if (PACKET_WITH_HEADER) else 0)] << 8) | data[3 + (4 if (PACKET_WITH_HEADER) else 0)]
        volt = data[1 + (4 if (PACKET_WITH_HEADER) else 0)] | ((data[0 + (4 if (PACKET_WITH_HEADER) else 0)] & 0x3) << 8)
        src = (data[0 + (4 if (PACKET_WITH_HEADER) else 0)] >> 6) & 0x1; #Source bit is no longer necessary



        moisture = -0.008547008547008548*volt+239.31623931623935 #Fahim's equation to scale packet from 0 to 100
        rssi = rfm9x.last_rssi
        #print("Raw Packet: {}\nID: {:X}\nSensor RSSI: {:X} -> {}\nRelay RSSI: {:X} -> {}\nData: {}/1023 -> {}\nSource: {:X}".format(rawpacket, id, sensorRSSI,hex16toSInt(sensorRSSI), rssi, rssi, volt, volt/1023.0, src))
        #if (src == 0x01): #Checking from source no longer necessary
        file.write("{},{},{},{},{},{}\n".format(datetime.now(),id,moisture, hex16toSInt(sensorRSSI), rssi, rawpacket))
        no_packet_start_time = time.time()

    #If buttonA is pressed, then exit the while loop.
    if (btnA.value == False):
        print("BtnA pressed")
        break 
    #If buttonB is pressed, do nothing (currently)
    if (btnB.value == False):
        print("BtnB pressed")
    #If buttonC is pressed, copy log to the flash drive
    if (btnC.value == False):
        print("BtnC pressed")
        file.close() #Close file. Flushes stream
        #The OS automatically mounts the drive, but folder name isn't always consistent as it's based on the drive name. 
        os.system('sudo umount /dev/sda1') #To create consistency, the drive is first unmounted
        os.system('sudo mount /dev/sda1 /mnt/usb') #Then the drive is mounted to a specific folder 
        os.system('sudo mv {0}/{1} /mnt/usb/{1}'.format(logDir, filename)) #Copy the files to the mount folder
        os.system('sudo umount /dev/sda1') #Unmount the drive
        print("SAFE TO REMOVE USB") #Notify user via console. This is not sufficient.
        file = open('{}/{}'.format(logDir, filename), 'w') #Open a new log file
        file.write("Time,UUID,Soil Moisture,RSSI (Sensor to Relay),RSSI (Relay to Base)\n") #Write the column headers to the new file.
        

file.close()




