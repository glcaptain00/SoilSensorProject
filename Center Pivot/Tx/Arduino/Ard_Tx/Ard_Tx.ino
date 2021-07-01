//Code influneced by Adafruit's example.
//Some of the variables added have been tweaked to follow the naming
//convention that I had already been using for other variables.

//Configurables
#define TX_POWER 23
#define PIN_SENSOR A1

#define RADIO_RST 2
#define RADIO_CS 4
#define RADIO_INT 3
#define RADIO_FREQ 915.0

//CONSTANTS
#define PACKET_LENGTH 4

#include <RH_RF95.h>
#include <SPI.h>

//UUID, don't touch. UUID: 4918bc6e-c881-11eb-b8bc-0242ac130003
uint8_t id = 0x00; //Used for Tx_FROM header byte
uint8_t target_relay = 0xF0; //Used for Tx_TO header byte
RH_RF95 rf95(RADIO_CS, RADIO_INT); //Creating global object for the radio

void setup() {
	//Setup pins
	pinMode(RADIO_RST, OUTPUT);
	digitalWrite(RADIO_RST, HIGH);
  
	Serial.begin(9600);
	//while (!Serial); //Initialize serial port. This waits for a serial monitor to be open

	//Resetting Radio
	Serial.println("Resetting radio...");
	digitalWrite(RADIO_RST, LOW);
	delay(10);
	digitalWrite(RADIO_RST, HIGH);
	delay(10);
	Serial.println("Radio reset.");
  
  
	while (!rf95.init()) //Initialize radio
	{
		Serial.println("Init failed");
		delay(5000);
	}
	if (!rf95.setFrequency(915.0)) //If the set frequency fails, it's out of range.
	{
		Serial.println("Frequency out of range.");
	}
	
	//Final radio configuration
	rf95.setTxPower(TX_POWER, false); //Set Tx power.
	rf95.setHeaderTo((uint8_t)0xF0);
	rf95.setHeaderFrom(id);

	Serial.println("Startup complete");
}

uint16_t voltage; 
uint8_t* data = new uint8_t[4];

void loop() {
  	// put your main code here, to run repeatedly:
	delay(500); //Delay in milliseconds.
	voltage = analogRead(PIN_SENSOR); 
	//In this packet: (Note: '?' represents the bit where the mentioned piece of data is stored.)
	//// RSSI:              0bXXXX_XXXX XXXX_XXXX ????_???? ????_????
	//// Sensor reading:    0bXXXX_XX?? ????_???? XXXX_XXXX XXXX_XXXX
	//// ID:                0bXX??_??XX XXXX_XXXX XXXX_XXXX XXXX_XXXX 
	//// Source:            0bX?XX_XXXX XXXX_XXXX XXXX_XXXX XXXX_XXXX
	data[3] = 0x00; //RSSI byte
	data[2] = 0x00; //RSSI byte
	data[1] = voltage & 0xFF;
 	data[0] = voltage >> 8;// | id << 2;
	Serial.print(data[0], HEX); Serial.print(" "); Serial.print(data[1], HEX); Serial.print(" "); Serial.print(data[2], HEX); Serial.print(" "); Serial.println(data[3], HEX);
	rf95.send(data, 4); //Send the data.
	rf95.waitPacketSent();
  //rf95.setHeaderFrom(id++);
}
