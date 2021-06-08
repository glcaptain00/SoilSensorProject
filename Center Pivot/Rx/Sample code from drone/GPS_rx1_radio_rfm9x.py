# Import Python System Libraries
import os
import time 
from time import sleep
from datetime import datetime
import serial
import threading
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
prev_packet = None

start = time.time()

# Time to run
PERIOD_OF_TIME = 20

# Setup GPS
gpsReader = serial.Serial("/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_7_-_GPS_GNSS_Receiver-if00", 9600, timeout = 5)
class GPS_TimeSync (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.hasFix = False
        self.lastLat = None
        self.lastLong = None
        self.synced = False

    def run(self):
        global gpsReader
        while self.running:
            line = gpsReader.readline().strip().decode('ascii')
            dat = line.split(',')
            if (dat[0] == "$GPGGA"):
                if(dat[1] != ""):
                    hours = dat[1][0:2]
                    minutes = dat[1][2:4]
                    seconds = dat[1][4:6]
                    curTime = datetime.utcnow()
                    #print("Syncing system time")
                    os.system('sudo date -u {:0>2d}{:0>2d}{}{}{}.{}'.format(curTime.month, curTime.day, hours, minutes, curTime.year, seconds))
                    self.hasFix = True
                    self.synced = True
                    self.lastLat = "{} {}".format(dat[2], dat[3]) if dat[2] != "" else "NO FIX"
                    self.lastLong = "{} {}".format(dat[4], dat[5]) if dat[4] != "" else "NO FIX"
                else:
                    print("Failed to sync time with GPS")
                    self.hasFix = False

gps = GPS_TimeSync()
gps.start()
while (gps.synced == False):
    display.fill(0)
    display.text('Waiting for initial',0, 0, 1)
    display.text('time sync...', 0, 10, 1)
    display.show()
    if (btnB.value == False):
        print("Skipping")
        break
else:
    print("Time synced or sync skipped")

temptime = datetime.utcnow()
filename = "/home/pi/logs/{:0>2d}-{:0>2d}-{:0>2d}_{:0>2d}-{:0>2d}_data_log.csv".format(temptime.month,temptime.day, temptime.year, temptime.hour, temptime.minute)
file = open(filename, "a")
i=0
if os.stat(filename).st_size == 0:
        file.write("Time,RSSI (dBm),Latitude,Longitude\n")
no_packet_start_time = time.time()

while True:
    
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi LoRa', 35, 0, 1)

    # check for packet rx
    packet = rfm9x.receive()
    if packet is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        display.fill(0)
        prev_packett = packet
        #Filtering out packets with non-digits. Bad data
        if prev_packett.isdigit():
                prev=float(prev_packett)
                #Convert packet's data to a scale of 0 to 100
                prev_packet=-0.008547008547008548*prev+239.31623931623935
                #packet_text = str(prev_packet, "utf-8")
                display.text('Moisture: ', 0, 0, 1)
                #display.text(packet_text, 25, 0, 1)
                display.text(format(prev_packet), 0, 10, 1)
                #print(prev_packett)
                print("\nRaw Data "+str(float(prev_packett)))
                print("Soil Moisture "+ str(prev_packet))
                received_power=rfm9x.last_rssi
                print("Receiver_Signal_Strength:{0} dB".format(received_power))
                #snr=rfm9x.last_snr
                #print("SNR:  "+str(snr))
                #received_pow = str(received_power, "utf-8")
                display.text('RX_Power: ', 1, 20, 2)
                display.text(format(received_power), 55, 20, 2)
                #time.sleep(0.1)
         

                #i=i+1
                now = datetime.utcnow()
                #file.write(str(now)+","+str(i)+","+str(-i)+","+str(i-10)+","+str(i+5)+","+str(i*i)+"\n")
                file.write("{},{},{},{}\n".format(str(now), received_power, gps.lastLat, gps.lastLong))
                file.flush()
    
    
    

    if  packet==None and time.time()>no_packet_start_time+0.5:
        file.write("{},{},{},{}\n".format(str(datetime.now()), "Packet Loss", gps.lastLat, gps.lastLong))
        file.flush()
        no_packet_start_time=time.time()
    display.show()
    #time.sleep(0.1)
    #If time has exceeded total runtime
    #if time.time() > start + PERIOD_OF_TIME : break


    #If buttonA is pressed, then exit the while loop.
    #   This will replace the previous if statement to exit based on time.
    ##  This allows us to stop when we are done flying the drone, not when the time is up
    if (btnA.value == False):
        print("BtnA pressed")
        break
    if (btnB.value == False):
        print("BtnB pressed")
    if (btnC.value == False):
        print("BtnC pressed")


file.close()
gps.running = False
gps.join()
display.fill(0)
display.text("Exited...", 15, 20, 1)
display.show()
#print("Finished")



