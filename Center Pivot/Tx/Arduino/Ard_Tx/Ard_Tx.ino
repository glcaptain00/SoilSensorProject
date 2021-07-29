//Code influneced by Adafruit's example.
//Some of the variables added have been tweaked to follow the naming
//convention that I had already been using for other variables.

//Configurables
#define TX_POWER 23
#define PIN_SENSOR A1
#define ECHO_WAIT 500 //Time in milliseconds to wait if an echo is heard
#define NO_ECHO_WAIT 5000 //Time in milliseconds to wait if no echo is heard

//These configure the arduino pins to function to the connected radio pins
#define RADIO_RST 2 	//Connect to the RST pin on the radio
#define RADIO_CS 4		//Connects to the Controller select 'CS'
#define RADIO_INT 3		//Connects to the GPIO 0 pin, 'G0'. Used for interrupts
//The following is a list of the rest of the pin connections
// RADIO -> ARDUINO
// MOSI -> 11
// MISO -> 12
// SCK -> 13
// GND -> GND
// VIN -> Technically, either 5V or 3.3V pin will work, but I used 5V

//CONSTANTS
#define PACKET_LENGTH 4 //Length of packet
#define RADIO_FREQ 915.0 //The frequency of the radio

//Important libraries for the code
#include <RH_RF95.h>
#include <SPI.h>

//ID configuration
uint8_t id = 0x00; //Used for Tx_FROM header byte
uint8_t target_relay = 0xF0; //Used for Tx_TO header byte


RH_RF95 rf95(RADIO_CS, RADIO_INT); //Creating global object for the radio

void setup() {
	//Setup pins
	pinMode(RADIO_RST, OUTPUT);
	digitalWrite(RADIO_RST, HIGH); //Radio chip resets when the RST pin is pulled low, so we set it high to avoid this
  
	Serial.begin(9600); //Begin serial IO
	//while (!Serial); //Initialize serial port. This waits for a serial monitor to be open, so it needs to be commented out when not debugging

	//Resetting Radio. Chip resets when RST pin is low
	Serial.println("Resetting radio...");
	digitalWrite(RADIO_RST, LOW);
	delay(10);
	digitalWrite(RADIO_RST, HIGH);
	delay(10);
	Serial.println("Radio reset.");
  
  
	while (!rf95.init()) //Initialize radio. Do not move past this step until the radio succesfully initializes.
	{
		Serial.println("Init failed");
		delay(5000);
	}

	if (!rf95.setFrequency(RADIO_FREQ)) //If the set frequency fails, it's out of range.
	{
		Serial.println("Frequency out of range.");
	}
	
	//Final radio configuration
	rf95.setTxPower(TX_POWER, false); //Set Tx power.
	rf95.setHeaderTo((uint8_t)0xF0); //Set destination of packets
	rf95.setHeaderFrom(id); //Set sender id

	Serial.println("Startup complete");
}

//Creating important variables outside of the loop so that their space in memory is constant.
uint16_t voltage;
uint8_t* data = new uint8_t[4];
uint8_t packet [4] = {}; //Array of bytes to store packet
bool msg = false;

void loop() {
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
	//Serial.print(data[0], HEX); Serial.print(" "); Serial.print(data[1], HEX); Serial.print(" "); Serial.print(data[2], HEX); Serial.print(" "); Serial.println(data[3], HEX);
	rf95.send(data, 4); //Send the data.
	rf95.waitPacketSent(); //Wait for sent
	
	//Untested, but layout of echo receive wait algo
	//msg = rf95.recv(packet, 4);
	//if (msg)
	//{
		//delay(ECHO_WAIT)
	//}
	//else
	//{
		//delay(NO_ECHO_WAIT)
	//}
}
