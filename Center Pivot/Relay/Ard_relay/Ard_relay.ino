//Configurables
#define TX_POWER 13

#include <RH_RF95.h>
#include <SPI.h>

RH_RF95 rf95;
void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  rf95.init();
  if (!rf95.setFrequency(915.0))
  {
    Serial.print("Frequency out of range.");
  }
  rf95.setTxPower(TX_POWER);

}

void loop() {
  // put your main code here, to run repeatedly:
  //receive packet
  uint8_t packet [4] = {}; //Array of bytes to store packet
  rf95.recv(packet, &packet);
  int16_t rssi = rf95.recv();

  if ((packet[0] >> 2) == 0b0)
  {
    packet[0] = packet[0] | 0x40;
    
    
    rf95.send(packet, 4);
  }
}
