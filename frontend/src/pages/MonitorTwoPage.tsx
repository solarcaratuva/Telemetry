import {Box, Paper, Typography} from "@mui/material";
import {useEffect, useState} from "react";

import OnePedalDrive from "../components/OnePedalDrive";
import {io} from "socket.io-client";
import ToggleButtons from "../components/ToggleButtons";
import AlertBox from "../components/AlertBox";
import RPM from "../components/RPM";
import BatteryTempGuage from "../components/BatteryTempGuage";
import CurrentGuage from "../components/NetCurrentGuage";
import {
    Update,
    StringData,
    StringUpdate,
    StringArrayData,
    StringArrayUpdate,
    BooleanUpdate,
    DataSet
} from './UpdateTypes';
import {Data as DataBase} from './UpdateTypes'
import {BooleanData as BooleanDataBase} from './UpdateTypes'
import PackVoltageGuage from "../components/PackVoltageGuage";
import ToggleButton from "@mui/material/ToggleButton";
import * as React from "react";

interface Data extends DataBase {
    pack_voltage: DataSet,
    pack_current: DataSet
}

interface BooleanData extends BooleanDataBase {
    brake_lights: number,
    is_charging_signal_status: number
}

const socket = io("http://localhost:5050");
const MAX_LENGTH = 50;

// TODO - add below for monitor one/two
//  all stuff from hud
//  rpm, voltage
const MonitorTwoPage = () => {
    const [data, setData] = useState<Data>({
        battery_temp: [],
        panel_temp: [],
        throttle: [],
        hazards: [],
        brake_lights: [],
        forward_en: [],
        motor_rpm: [],
        pack_current: [],
        pack_voltage: [],
        high_temperature: [],
    });

    const [stringData, setStringData] = useState<StringData>({
        gear_state: [],
        hazard_state: [],
        turn_state: [],
        motor_faults: []
    });

    const [stringArrayData, setStringArrayData] = useState<StringArrayData>({
        BPSError: [],
        MotorControllerError: [],
        PowerAuxError: []
    });

    const [booleanData, setBooleanData] = useState<BooleanData>({
        left_turn_signal: 0,
        right_turn_signal: 0,
        forward_en: 0,
        brake_lights: 0,
        headlights: 0,
        hazards: 0,
        reverse_en: 0,
        is_charging_signal_status: 0
    });

    const [time, setTime] = useState(new Date().toLocaleTimeString());

    useEffect(() => {
        const intervalId = setInterval(() => {
            setTime(new Date().toLocaleTimeString());
        }, 1000);
        return () => {
            clearInterval(intervalId)
        };
    }, []);

    const [leftBlinker, setLeftBlinker] = useState(false);
    const [rightBlinker, setRightBlinker] = useState(false);

    useEffect(() => {
        //Attaches socket listeners for each value of the data object on mount
        Object.keys(data).forEach((name) => {
            socket.on(name, (update: Update) => {
                setData((oldData) => {
                    const updatedData = {
                        ...oldData,
                        [name]: [
                            ...oldData[name as keyof Data],
                            {value: update.number, timestamp: new Date(update.timestamp)},
                        ],
                    };
                    if (updatedData[name as keyof Data].length > MAX_LENGTH) {
                        updatedData[name as keyof Data] = updatedData[name as keyof Data].slice(-MAX_LENGTH);
                    }
                    return updatedData;
                });
            });
        });

        Object.keys(stringData).forEach((name) => {
            socket.on(name, (update: StringUpdate) => {
                setStringData((oldData) => {
                    const updatedData = {
                        ...oldData,
                        [name]: [
                            ...oldData[name as keyof StringData],
                            {value: update.string, timestamp: new Date(update.timestamp)},
                        ],
                    };
                    if (updatedData[name as keyof StringData].length > MAX_LENGTH) {
                        updatedData[name as keyof StringData] = updatedData[name as keyof StringData].slice(-MAX_LENGTH);
                    }
                    return updatedData;
                });
            });
        });

        (Object.keys(stringArrayData) as Array<keyof StringArrayData>).forEach((name) => {
            socket.on(name, (update: StringArrayUpdate) => {
                setStringArrayData((oldData) => {
                    oldData[name] = update.array;
                    return oldData;
                });
            });
        });

        Object.keys(booleanData).forEach((name) => {
            socket.on(name, (update: BooleanUpdate) => {
                console.log("update" + name + " to " + update.number);
                setBooleanData((oldData) => {
                    oldData[name as keyof BooleanData] = update.number;
                    return oldData;
                    // return {...oldData, [name as keyof BooleanData]: update.number};
                });
            });
        });

        //Removes all socket listeners for each value of the data object on unmount
        //This is to prevent multiple listeners from being attached to the same value
        return () => {
            Object.keys(data).forEach((name) => {
                socket.off(name);
            });
            Object.keys(stringData).forEach((name) => {
                socket.off(name);
            });
            Object.keys(stringArrayData).forEach((name) => {
                socket.off(name);
            });
            Object.keys(booleanData).forEach((name) => {
                socket.off(name);
            });
        };
    }, []);

    return (
        <Box p="16px" height="100vh" boxSizing="border-box">
            {/* Page is vertically centered and will adapt based on actual component sizes */}
            <Box
                height="100%"
                display="flex"
                flexDirection="column"
                gap="16px"
                justifyContent="center"
            >
                <Box
                    sx={{
                        display: "flex",
                        justifyContent: "space-around",
                        gap: "16px",
                        height: "33vh",
                    }}
                >
                    <BatteryTempGuage
                        temp={data.high_temperature.length !== 0 ? data.high_temperature[data.high_temperature.length - 1].value : 0}
                        darkMode={false}/>
                    <CurrentGuage
                        current={data.pack_current.length !== 0 ? data.pack_current[data.pack_current.length - 1].value : 0}
                        darkMode={false}/>
                    <PackVoltageGuage
                        voltage={data.pack_voltage.length !== 0 ? data.pack_voltage[data.pack_voltage.length - 1].value : 0}/>

                </Box>
                <Box sx={{display: "flex", gap: "16px", width: "100%"}}>
                    <Box
                        style={{ marginTop: "30px" }}
                        sx={{
                            display: "flex",
                            justifyContent: "space-around",
                            gap: "16px",
                            width: "100%",
                        }}
                    >
                        <Box
                            sx={{
                                display: "flex",
                                flexDirection: "column",
                                justifyContent: "space-around",
                                gap: "16px",
                                height: "40vh",
                                flex: "1 0 0",
                            }}
                        >
                            <ToggleButtons
                                leftOn={booleanData.forward_en === 1}
                                rightOn={booleanData.reverse_en === 1}
                                left={"Forward"}
                                right={"Reverse"}
                                label={"Gear"}
                            />
                            <Box
                                sx={{
                                    display: "flex",
                                    flexDirection: "row",
                                    justifyContent: "center",
                                    gap: "15px",
                                    height: "40vh",
                                    flex: "1 0 0",
                                }}
                            >
                                <ToggleButtons
                                    leftOn={booleanData.brake_lights === 0}
                                    rightOn={booleanData.brake_lights === 1}
                                    left={"Off"}
                                    right={"On"}
                                    label={"Brake Lights"}
                                />
                                <ToggleButtons
                                    leftOn={booleanData.headlights === 0}
                                    rightOn={booleanData.headlights === 1}
                                    left={"Off"}
                                    right={"On"}
                                    label={"Head Lights"}
                                />
                            </Box>
                            <ToggleButtons
                                leftOn={booleanData.hazards === 1 || booleanData.left_turn_signal === 1}
                                rightOn={booleanData.hazards === 1 || booleanData.right_turn_signal === 1}
                                left={"Left"}
                                right={"Right"}
                                label={"Turn Signal"}
                            />
                            <ToggleButton disabled value={"charging"} selected={booleanData.is_charging_signal_status==1} aria-label="left aligned">
                                Battery Charging
                            </ToggleButton>
                        </Box>
                        <Box
                            sx={{
                                display: "flex",
                                flexDirection: "column",
                                justifyContent: "space-around",
                                gap: "16px",
                                flex: "3 0 0",
                            }}
                        >
                            <OnePedalDrive
                                value={data.throttle.length != 0 ? data.throttle[data.throttle.length - 1].value : 50}/>
                            <Box
                                sx={{
                                    display: "flex",
                                    justifyContent: "space-around",
                                    gap: "16px",
                                }}
                            >
                                {/* Replace this paper component with motor faults */}

                                <AlertBox
                                    data={(booleanData.hazards === 1 && booleanData.headlights == 1 ? ["BMS Error"] : [] as string[]).concat(stringArrayData.BPSError, stringArrayData.MotorControllerError, stringArrayData.PowerAuxError)}/>

                                {/* Replace this paper component with fifa chart */}
                                <Box
                                    sx={{
                                        flex: "1 0 0",
                                        display: "flex",
                                        alignItems: "flex-start",
                                        justifyContent: "center",
                                        height: "calc(25vh - 8px)"
                                    }}
                                    marginBottom={10}
                                >
                                    <RPM
                                        rpm={data.motor_rpm.length !== 0 ? data.motor_rpm[data.motor_rpm.length - 1].value : 0}
                                        darkMode={false}/>
                                </Box>
                            </Box>
                        </Box>
                    </Box>
                </Box>
            </Box>
        </Box>
    );
};

export default MonitorTwoPage;
