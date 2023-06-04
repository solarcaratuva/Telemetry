export type DataSet = { value: number; timestamp: Date }[];

export interface Data {
    motor_rpm: DataSet
    battery_temp: DataSet;
    panel_temp: DataSet;
    throttle: DataSet;
    hazards: DataSet;
    brake_lights: DataSet;
    forward_en: DataSet;
    total_current: DataSet;
    high_temperature: DataSet;
}

export interface Update {
    number: number;
    timestamp: string;
}

export type StringDataSet = { value: string; timestamp: Date }[];

export interface StringData {
    gear_state: StringDataSet;
    hazard_state: StringDataSet;
    turn_state: StringDataSet;
    motor_faults: StringDataSet
}

export interface StringUpdate {
    string: string;
    timestamp: string;
}

export interface StringArrayData {
    BPSError: string[],
    MotorControllerError: string[],
    PowerAuxError: string[]
}

export interface StringArrayUpdate {
    array: string[];
    timestamp: string
}

export interface BooleanData {
    left_turn_signal: number,
    right_turn_signal: number,
    forward_en: number,
    reverse_en: number
}

export interface BooleanUpdate {
    number: number,
    timestamp: number
}