import {Box} from "@mui/material";
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
    DataSet
} from './UpdateTypes';
import {Data as DataBase} from './UpdateTypes'
import PackVoltageGuage from "../components/PackVoltageGuage";

interface Data extends DataBase {
    panel1_voltage: DataSet,
    panel2_voltage: DataSet,
    panel3_voltage: DataSet,
    panel4_voltage: DataSet,
    panel1_temp: DataSet,
    panel2_temp: DataSet,
    panel3_temp: DataSet,
    panel4_temp: DataSet
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
        high_temperature: [],
        panel1_voltage: [],
        panel2_voltage: [],
        panel3_voltage: [],
        panel4_voltage: [],
        panel1_temp: [],
        panel2_temp: [],
        panel3_temp: [],
        panel4_temp: []
    });

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

        //Removes all socket listeners for each value of the data object on unmount
        //This is to prevent multiple listeners from being attached to the same value
        return () => {
            Object.keys(data).forEach((name) => {
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
                    <BatteryTempGuage
                        temp={data.high_temperature.length !== 0 ? data.high_temperature[data.high_temperature.length - 1].value : 0}
                        darkMode={false}/>
                    <CurrentGuage
                        current={data.pack_current.length !== 0 ? data.pack_current[data.pack_current.length - 1].value : 0}
                        darkMode={false}/>
                    <PackVoltageGuage
                        voltage={data.pack_current.length !== 0 ? data.pack_current[data.pack_current.length - 1].value : 0}/>

                </Box>
                <Box
                    style={{ marginTop: "30px" }}
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
                    <BatteryTempGuage
                        temp={data.high_temperature.length !== 0 ? data.high_temperature[data.high_temperature.length - 1].value : 0}
                        darkMode={false}/>
                    <CurrentGuage
                        current={data.pack_current.length !== 0 ? data.pack_current[data.pack_current.length - 1].value : 0}
                        darkMode={false}/>
                    <PackVoltageGuage
                        voltage={data.pack_current.length !== 0 ? data.pack_current[data.pack_current.length - 1].value : 0}/>
                </Box>
            </Box>
        </Box>
    );
};

export default MonitorTwoPage;
