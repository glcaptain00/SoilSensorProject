#UUID
#uuid = "ecb61540-c554-11eb-8529-0242ac130003" This is the cleaner, clearer UUID representation
uuid = 0xecb61540c55411eb85290242ac130003 #This representation is purely for bitmasking purposes.

# Import Python System Libraries
import time
# Import Blinka Libraries
import busio
from digitalio import DigitalInOut
import board
# Import the SSD1306 module.
import adafruit_ssd1306
# Import RFM9x
import adafruit_rfm9x

# Import ADC
from ADCPi import ADCPi

adc=ADCPi(0x68,0x69,16)

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
rfm9x.tx_power = 23
prev_packet = None

while True:
    packet = None
    # draw a box to clear the image
    #display.fill(0)
    #display.text('RasPi LoRa Tx', 35, 0, 1)

    # Read ADC
    voltage=adc.read_raw(1)
    print(voltage)
    
    #bandwidth=rfm9x.signal_bandwidth
    #print(bandwidth)
    
    voltage = voltage << 1
    packet = uuid << 17 | voltage
    packet = packet & ~1

    
    data = bytes("{}{}{}".format(uuid,voltage,"0"),"utf-8")
    rfm9x.send(data)
    #display.text('Data Sent', 25, 15, 1)


    #display.show()
    time.sleep(0.5)
