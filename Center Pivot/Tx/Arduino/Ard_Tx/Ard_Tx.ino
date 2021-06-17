//Configurables
#define TX_POWER 13
#define PIN_SENSOR A1

//CONSTANTS
#define PACKET_LENGTH 18

#include <RH_RF95.h>
#include <SPI.h>

//UUID, don't touch. UUID: 4918bc6e-c881-11eb-b8bc-0242ac130003
uint8_t id = 0x0;
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
	int voltage = analogRead(PIN_SENSOR); //FIXME: This needs to read from the sensor, not be hard coded.
	uint8_t* data = new uint8_t[4];
 
	data[3] = 0x00;
  	data[2] = 0x00; //RSSI byte
  	data[1] = voltage & 0xFF;
 	data[0] = voltage >> 8 | id << 2;
	rf95.send(data, 4); //Send the data.
}
