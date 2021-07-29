#include <RadioHead.h>

//Configurables
#define TX_POWER 23 //23 IS MAX
#define RADIO_FREQ 915.0

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

uint8_t relay_id = 0xF0;
uint8_t base_id = 0xFE;

//End of Configurables

//Including important libraries
#include <RH_RF95.h>
#include <SPI.h>

//Creating radio driver
RH_RF95 rf95(RADIO_CS, RADIO_INT);

void setup() {
  Serial.begin(9600); //Begin serial IO
 
  //Setup pins
  pinMode(RADIO_RST, OUTPUT);
  digitalWrite(RADIO_RST, HIGH); //Radio chip resets when the RST pin is pulled low, so we set it high to avoid this

  //Resetting Radio
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

  if (!rf95.setFrequency(RADIO_FREQ)) //Set the frequency to RADIO_FREQ. If it fails, this if block will run
  {
    Serial.print("Frequency out of range.");
    while (1); //Infinite loop that does nothing. If the frequency is invalid, the code will hang here.
  }
  
  //Final radio configuration
  rf95.setTxPower(TX_POWER, false); //Setting transmit power. DO NOT CHANGE THE 'false'.
  rf95.setThisAddress(relay_id); //Set the address of this radio
  rf95.setHeaderTo(base_id); //Set the address of the radio that should receive this radio's packets
  rf95.setHeaderFrom(relay_id); //Set the FROM byte to be this radio's address.
  
  Serial.println("Setup complete");

}

//Creating variables outside of the loop to avoid memory leaks
int16_t rssi = 0;
bool msg;
uint8_t packet [4] = {}; //Array of bytes to store packet

void loop() {
  msg = rf95.recv(packet, 4); //Receive packet. 'msg' will be true if a message is received.
  rssi = rf95.lastRssi(); //Stores the RSSI value of the last received message

  if (msg) //If a message was succesfully received
  {
    //if ((packet[0] >> 2) & 0b1 == 0b0)
    //{
      //Serial.print(packet[0], HEX); Serial.print(" "); Serial.print(packet[1], HEX); Serial.print(" "); Serial.print(packet[2], HEX); Serial.print(" "); Serial.println(packet[3], HEX);
      packet[0] = packet[0] | 0x40; //Set the SRC bit of the packet 
      
      //Set the values of the RSSI bytes
      packet[2] = rssi >> 8; 
      packet[3] = rssi & 0xFF;
      
      //Send packet and wait
      rf95.send(packet, 4);
      rf95.waitPacketSent();
    //}
  }
  
}
