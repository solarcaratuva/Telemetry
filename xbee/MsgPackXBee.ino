// Solar Car @ UVA | Telemetry
// 23 February 2020

#include <ArduinoJson.h>
#include <SoftwareSerial.h>

#define rX 7
#define tX 8

SoftwareSerial xbee = SoftwareSerial(rX,tX);

const int capacity = JSON_OBJECT_SIZE(54);

StaticJsonDocument<capacity> telemetryData;

void changeDoc() {
  // Timestamp
  telemetryData.t = millis(); 
  
  // BMS numbers
  telemetryData.b[0] = (float)random(25,30);
  telemetryData.b[1] = (float)random(80,100);
  telemetryData.b[2] = (float)random(90,100);
  telemetryData.b[3] = random(65,70);
  telemetryData.b[4] = random(55,60);
  telemetryData.b[5] = random(80,90);
  telemetryData.b[6] = random(50,60);
  telemetryData.b[7] = random(60,70);

  // BMS bools
  telemetryData.c[0] = false;
  telemetryData.c[1] = false;
  telemetryData.c[2] = false;
  telemetryData.c[3] = false;
  telemetryData.c[4] = false;
  telemetryData.c[5] = false;
  telemetryData.c[6] = false;
  telemetryData.c[7] = false;
  
  // BMS faults
  telemetryData.f[0] = false;
  telemetryData.f[1] = false;
  telemetryData.f[2] = false;
  telemetryData.f[3] = false;
  telemetryData.f[4] = false;
  telemetryData.f[5] = false;
  telemetryData.f[6] = false;
  telemetryData.f[7] = false;
  telemetryData.f[8] = false;
  telemetryData.f[9] = false;
  telemetryData.f[10] = false;
  telemetryData.f[11] = false;
  telemetryData.f[12] = false;
  telemetryData.f[13] = false;
  telemetryData.f[14] = false;
  telemetryData.f[15] = false;
  telemetryData.f[16] = false;
  telemetryData.f[17] = false;
  telemetryData.f[18] = false;
  telemetryData.f[19] = false;
  telemetryData.f[20] = false;

  // KLS status
  telemetryData.k[0] = random(100,150);
  telemetryData.k[1] = (float)random(50,60);
  telemetryData.k[2] = (float)random(80,100);
  telemetryData.k[3] = (float)random(50,60);
  telemetryData.k[4] = random(90,100);
  telemetryData.k[5] = random(80,90);
  telemetryData.k[6] = false;
  telemetryData.k[7] = false;

  //KLS switch
  telemetryData["sa"] = false;
  telemetryData["sb"] = false;
  telemetryData["sc"] = false;
  telemetryData["sd"] = false;
  telemetryData["se"] = false;
  telemetryData["sf"] = false;
  telemetryData["sg"] = false;
  telemetryData["sh"] = false;
}

void setup() {  
  pinMode(rX,INPUT);
  pinMode(tX,OUTPUT);
  xbee.begin(9600);
}

void loop() {
  changeDoc();
  serializeMsgPack(telemetryData,xbee);
  delay(2000);
}
