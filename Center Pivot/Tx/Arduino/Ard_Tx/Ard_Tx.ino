//Configurables
#define TX_POWER 13
#define PIN_SENSOR 1

//CONSTANTS
#define PACKET_LENGTH 18

#include <RH_RF95.h>
#include <SPI.h>

//UUID, don't touch. UUID: 4918bc6e-c881-11eb-b8bc-0242ac130003
uint8_t uuid [16] = {0x49, 0x18, 0xbc, 0x6e, 0xc8, 0x81, 0x11, 0xeb, 0xb8, 0xbc, 0x02, 0x42, 0xac, 0x13, 0x00, 0x03};

RH_RF95 rf95; //Creating global object for the radio
void setup() {
	Serial.begin(9600); //Initialize serial port.

	rf95.init(); //Initialize radio
	if (!rf95.setFrequency(915.0)) //If the set frequency fails, it's out of range.
	{
		Serial.print("Frequency out of range.");
	}
	rf95.setTxPower(TX_POWER); //Set Tx power.
}

void loop() {
  // put your main code here, to run repeatedly:
	delay(500); //Delay in milliseconds.
	int voltage = 0x0ABC; //FIXME: This needs to read from the sensor, not be hard coded.
	uint8_t data [PACKET_LENGTH] = {}; //Create an array of PACKET_LENGTH size. See 'constants' macro section (at top)
	uint8_t of = 0x00; //Store overflow variable for right shift compression
	uint8_t next_of = 0x00; //temp overflow. Necessary for cycling without creating a new array.
	uint16_t temp = (voltage << 1) | 0x0000; //Left shifting one gives the overflow of right shifting 7
	data[PACKET_LENGTH - 1] = temp & 0xFF; //Src bit is 0, so 
	data[PACKET_LENGTH - 2] = temp >> 8;
	for (int i = PACKET_LENGTH - 3; i >= 0; i--)
	{
		data[i+1] = data[i+1] | (uuid[i] << 5);
		data[i] = uuid[i] >> 3;
	}
	for (int i = 0; i < PACKET_LENGTH; i++)
	{
		cout << hex << +data[i] << " ";
	}
	rf95.send(data, sizeof(data)); //Send the data.
}
