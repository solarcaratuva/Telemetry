#ifndef ArduinoCanParser_h
#define ArduinoCanParser_h

#include <Arduino.h>
#include "bps.h"
#include "motor_controller.h"
#include "mppt.h"
#include "rivanna2.h"

class ArduinoCanParser {
    public:
        ArduinoCanParser();
        void begin();
        void parseCanMessage(CAN_message_t message);

    private:
        uint16_t BPSPackInfo = 1030;
        uint16_t BPSCellVoltage = 1046;
        uint16_t BPSCellTemperature = 1062;
        uint16_t BPSError = 262;

        uint16_t MG0Status = 384;
        uint16_t MG1Status = 385;
        uint16_t MG0OutputVoltageInputPower = 640;
        uint16_t MG1OutputVoltageInputPower = 641;
        uint16_t MG0PCBMOSFETTemperature = 1152;
        uint16_t MG1PCBMOSFETTemperature = 1153;

        uint16_t MotorControllerFrameRequest = 818;
        uint16_t MotorControllerPowerStatus = 805;
        uint16_t MotorControllerDriveStatus = 789;
        uint16_t MotorControllerError = 277;

        uint16_t PowerAuxError = 291;
        uint16_t ECUMotorCommands = 513;
        uint16_t ECUPowerAuxCommands = 769;
        uint16_t SolarCurrent = 1076;
        uint16_t SolarVoltage = 1092;
        uint16_t SolarTemp = 1108;
        uint16_t SolarPhoto = 1124;

};

#endif