#include <Arduino.h>
#include "ArduinoCanParser.h"

ArduinoCanParser::ArduinoCanParser();
void ArduinoCanParser::begin();

void ArduinoCanParser::parseCanMessage(CAN_message_t message) {
    uint16_t id = message.id;
    uint8_t data[8] = message.data;
    uint8_t len = message.len;

    if(id == BPSPackInfo) {
        bps_bps_pack_information_t packInfo;
        bps_bps_pack_information_unpack(&packInfo, data, len);
    }
    else if(id == BPSCellVoltage) {
        bps_bps_cell_voltage_t cellVoltage;
        bps_bps_cell_voltage_unpack(&cellVoltage, data, len);
    }
    else if(id == BPSCellTemperature) {
        bps_bps_cell_temperature_t cellTemperature;
        bps_bps_cell_temperature_unpack(&cellTemperature, data, len);
    }
    else if(id == BPSError) {
        bps_bps_error_t error;
        bps_bps_error_unpack(&error, data, len);
    }
    else if(id == MG0Status) {
        motor_controller_status_t status;
        motor_controller_status_unpack(&status, data, len);
    }
    else if(id == MG1Status) {
        motor_controller_status_t status;
        motor_controller_status_unpack(&status, data, len);
    }
    else if(id == MG0OutputVoltageInputPower) {
        motor_controller_output_voltage_input_power_t outputVoltageInputPower;
        motor_controller_output_voltage_input_power_unpack(&outputVoltageInputPower, data, len);
    }
    else if(id == MG1OutputVoltageInputPower) {
        motor_controller_output_voltage_input_power_t outputVoltageInputPower;
        motor_controller_output_voltage_input_power_unpack(&outputVoltageInputPower, data, len);
    }
    else if(id == MG0PCBMOSFETTemperature) {
        motor_controller_pcb_mosfet_temperature_t pcbMosfetTemperature;
        motor_controller_pcb_mosfet_temperature_unpack(&pcbMosfetTemperature, data, len);
    }
    else if(id == MG1PCBMOSFETTemperature) {
        motor_controller_pcb_mosfet_temperature_t pcbMosfetTemperature;
        motor_controller_pcb_mosfet_temperature_unpack(&pcbMosfetTemperature, data, len);
    }
    else if(id == MotorControllerFrameRequest) {
        motor_controller_frame_request_t frameRequest;
        motor_controller_frame_request_unpack(&frameRequest, data, len);
    }
    else if(id == MotorControllerPowerStatus) {
        motor_controller_power_status_t powerStatus;
        motor_controller_power_status_unpack(&powerStatus, data, len);
    }
    else if(id == MotorControllerDriveStatus) {
        motor_controller_drive_status_t driveStatus;
        motor_controller_drive_status_unpack(&driveStatus, data, len);
    }
    else if(id == MotorControllerError) {
        motor_controller_error_t error;
        motor_controller_error_unpack(&error, data, len);
    }
    else if(id == PowerAuxError) {
        power_aux_error_t error;
        power_aux_error_unpack(&error, data, len);
    }
    else if(id == ECUMotorCommands) {
        ecu_motor_commands_t commands;
        ecu_motor_commands_unpack(&commands, data, len);
    }
    else if(id == ECUPowerAuxCommands) {
        ecu_power_aux_commands_t commands;
        ecu_power_aux_commands_unpack(&commands, data, len);
    }
    else if(id == SolarCurrent) {
        mppt_solar_current_t current;
        mppt_solar_current_unpack(&current, data, len);
    }
    else if(id == SolarVoltage) {
        mppt_solar_voltage_t voltage;
        mppt_solar_voltage_unpack(&voltage, data, len);
    }
    else if(id == SolarTemp) {
        mppt_solar_temp_t temp;
        mppt_solar_temp_unpack(&temp, data, len);
    }
    else if(id == SolarPhoto) {
        mppt_solar_photo_t photo;
        mppt_solar_photo_unpack(&photo, data, len);
    }   
}