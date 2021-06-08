
# Import Python System Libraries
import time
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
rfm9x.tx_power = 23
prev_packet = None

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
        prev_packet = packet
        packet_text = str(prev_packet, "utf-8")
        display.text('RX: ', 0, 0, 1)
        display.text(packet_text, 25, 0, 1)
        #received_power=rfm9x.last_rssi
        #print("Receiver_Signal_Strength:{0} dB".format(received_power))
        time.sleep(0.1)

    


    display.show()
    time.sleep(0.1)




