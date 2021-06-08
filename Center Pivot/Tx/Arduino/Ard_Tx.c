//Arduino Macros
#define SCLK_PIN 13
#define MISO_PIN 12
#define MOSI_PIN 11
#define CS_PIN 4
#define RST_PIN 2
#define IRQ_PIN 3

//RMF9x register macros
#define REG_FIFO 0x00
#define REG_OP_MODE 0x01

//OpMode bit Macros
#define LORA_MODE 0x80
#define ACCESS_SHARED_REG 0x40
#define LOW_FREQ_MODE_ON 0x08
#define MODE_SLEEP 0x00
#define MODE_STDBY 0x01
#define MODE_FSTX 0x02
#define MODE_TX 0x03
#define MODE_FSRX 0x04
#define MODE_RX_CONT 0x05
#define MODE_RX_SING 0x06
#define MODE_CAD 0x07

#include <SPI.h>

void write_MOSI(byte addr, byte dat)
{
	//Chip reads first byte as addr, second byte as data. Transfer in that order
	SPI.transfer(addr);
	SPI.transfer(dat);
}

void setup() {
	SPI.begin();
	regOp = LORA_MODE | LOW_FREQ_MODE_ON | MODE_TX; //Create byte to adjust operation to Low Freq LoRa radio in Transmit mode
	write_MOSI(REG_OP_MODE, regOp); //Send the created byte
	
	
}

void loop() {
  // put your main code here, to run repeatedly:

}