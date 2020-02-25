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
  telemetryData["t"] = millis(); 
  
  // BMS numbers
  telemetryData["ba"] = (float)random(25,30);
  telemetryData["bb"] = (float)random(80,100);
  telemetryData["bc"] = (float)random(90,100);
  telemetryData["bd"] = random(65,70);
  telemetryData["be"] = random(55,60);
  telemetryData["bf"] = random(80,90);
  telemetryData["bg"] = random(50,60);
  telemetryData["bh"] = random(60,70);

  // BMS bools
  telemetryData["ca"] = false;
  telemetryData["cb"] = false;
  telemetryData["cc"] = false;
  telemetryData["cd"] = false;
  telemetryData["ce"] = false;
  telemetryData["cf"] = false;
  telemetryData["cg"] = false;
  telemetryData["ch"] = false;
  
  // BMS faults
  telemetryData["fa"] = false;
  telemetryData["fb"] = false;
  telemetryData["fc"] = false;
  telemetryData["fd"] = false;
  telemetryData["fe"] = false;
  telemetryData["ff"] = false;
  telemetryData["fg"] = false;
  telemetryData["fh"] = false;
  telemetryData["fi"] = false;
  telemetryData["fj"] = false;
  telemetryData["fk"] = false;
  telemetryData["fl"] = false;
  telemetryData["fm"] = false;
  telemetryData["fn"] = false;
  telemetryData["fo"] = false;
  telemetryData["fp"] = false;
  telemetryData["fq"] = false;
  telemetryData["fr"] = false;
  telemetryData["fs"] = false;
  telemetryData["ft"] = false;
  telemetryData["fu"] = false;

  // KLS status
  telemetryData["ka"] = random(100,150);
  telemetryData["kb"] = (float)random(50,60);
  telemetryData["kc"] = (float)random(80,100);
  telemetryData["kd"] = (float)random(50,60);
  telemetryData["le"] = random(90,100);
  telemetryData["kf"] = random(80,90);
  telemetryData["kg"] = false;
  telemetryData["kf"] = false;

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
