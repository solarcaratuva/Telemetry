import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState } from "react";

import OnePedalDrive from "../components/OnePedalDrive";
import { io } from "socket.io-client";
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
    BooleanData,
    BooleanUpdate,
    DataSet
} from './UpdateTypes';
import {Data as DataBase} from './UpdateTypes'

interface Data extends DataBase {
    panel1_voltage: DataSet,
    panel2_voltage: DataSet,
    panel3_voltage: DataSet,
    panel4_voltage: DataSet,
    panel1_temp: DataSet,
    panel2_temp: DataSet,
    panel3_temp: DataSet,
    panel4_temp: DataSet,
    pack_voltage: DataSet,
    pack_current: DataSet
}

const socket = io("http://localhost:5050");
const MAX_LENGTH = 50;

// TODO - add below for monitor one/two
//  all stuff from hud
//  rpm, voltage
const MonitorOnePage = () => {
    const [data, setData] = useState<Data>({
        battery_temp: [],
        panel_temp: [],
        throttle: [],
        hazards: [],
        brake_lights: [],
        forward_en: [],
        motor_rpm: [],
        total_current: [],
        high_temperature: [],
        panel1_voltage: [],
        panel2_voltage: [],
        panel3_voltage: [],
        panel4_voltage: [],
        panel1_temp: [],
        panel2_temp: [],
        panel3_temp: [],
        panel4_temp: [],
        pack_voltage: [],
        pack_current: []
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
        hazards: 0,
        reverse_en: 0
    });

    const [time, setTime] = useState(new Date().toLocaleTimeString());

    useEffect(()=>{
        const intervalId = setInterval(()=>{
            setTime(new Date().toLocaleTimeString());
        }, 1000);
        return ()=>{clearInterval(intervalId)};
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
              { value: update.number, timestamp: new Date(update.timestamp) },
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
              { value: update.string, timestamp: new Date(update.timestamp) },
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
          {/* Replace this paper component with motor temp */}
          <Paper
            sx={{
              flex: "1 0 0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Typography>Motor Temp</Typography>
          </Paper>
          <RPM  rpm={data.motor_rpm[data.motor_rpm.length - 1].value} darkMode={false}/>
          {/* Replace this paper component with battery pack temp */}

          <BatteryTempGuage temp={data.high_temperature.length !== 0 ? data.high_temperature[data.high_temperature.length - 1].value : 0} darkMode={false}/>
          <CurrentGuage current={data.total_current.length !== 0 ? data.total_current[data.total_current.length - 1].value : 0} darkMode={false} />
        </Box>
        <Box sx={{ display: "flex", gap: "16px", width: "100%" }}>
          <Box
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
                leftOn = {false}
                rightOn = {true}
                left={"Low"}
                right={"High"}
                label={"Gear:"}
              />
              <ToggleButtons
                leftOn = {false}
                rightOn = {true}
                left={"Off"}
                right={"On"}
                label={"Hazard State:"}
              />
              <ToggleButtons
                leftOn = {false}
                rightOn = {true}
                left={"Left"}
                right={"Right"}
                label={"Turn Signal:"}
              />
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
              <OnePedalDrive value={ data.throttle.length != 0 ? data.throttle[data.throttle.length - 1].value : 50 } />
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-around",
                  gap: "16px",
                }}
              >
                {/* Replace this paper component with motor faults */}

                  <AlertBox data={stringArrayData.BPSError.concat(stringArrayData.MotorControllerError, stringArrayData.PowerAuxError)}/>

                {/* Replace this paper component with fifa chart */}
                <Paper
                  sx={{
                    flex: "1 0 0",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    height: "calc(25vh - 8px)",
                  }}
                >
                  <Typography>Fifa Chart</Typography>
                </Paper>
              </Box>
            </Box>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default MonitorOnePage;
