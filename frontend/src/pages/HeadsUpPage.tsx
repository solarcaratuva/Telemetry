import {Box} from "@mui/material";
import React, {useEffect, useState} from "react";
import VideoFeed from "../components/VideoFeed";
import OnePedalDrive from "../components/OnePedalDrive";
import {io} from "socket.io-client";
import AlertBox from "../components/AlertBox";
import RPM from "../components/RPM";
import BatteryTempGuage from "../components/BatteryTempGuage";
import MPHandTurnSignal from "../components/MPHandTurnSignal";
import GearState from "../components/GearState";
import BatteryDischarge from "../components/BatteryDischargeGuage";

const socket = io("http://localhost:5050");
const MAX_LENGTH = 50;

type DataSet = { value: number; timestamp: Date }[];
interface Data {
  car_speed: DataSet;
  battery_temp: DataSet;
  panel_temp: DataSet;
  throttle: DataSet;
  left_turn_signal: DataSet;
  right_turn_signal: DataSet;
  forward_en: DataSet;
  motor_rpm: DataSet;
}

interface Update {
  number: number;
  timestamp: string;
}

type StringDataSet = { value: string; timestamp: Date }[];
interface StringData {
  gear_state: StringDataSet;
  hazard_state: StringDataSet;
  turn_state: StringDataSet;
  motor_faults: StringDataSet
}
interface StringUpdate {
  string: string;
  timestamp: string;
}

interface StringArrayData {
  BPSError: string[],
  MotorControllerError: string[],
  PowerAuxError: string[]
}

interface StringArrayUpdate {
  array: string[];
  timestamp: string
}

const HeadsUpPage = () => {
  const [data, setData] = useState<Data>({
    car_speed: [],
    battery_temp: [],
    panel_temp: [],
    throttle: [],
    left_turn_signal: [],
    right_turn_signal: [],
    forward_en: [],
    motor_rpm: []
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

  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(()=>{
    const intervalId = setInterval(()=>{
      setTime(new Date().toLocaleTimeString());
    }, 1000);
    return ()=>{clearInterval(intervalId)};
  }, []);

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
        console.log(name + " : ");
        update.array.forEach(console.log);
        setStringArrayData((oldData) => {
          console.log("len " + update.array.length);
          oldData[name] = update.array;
          return oldData;
        });
        stringArrayData.BPSError.forEach((val) => {
          console.log("bps err: " + val);
        })
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
    <Box  height="100vh" boxSizing="border-box" bgcolor = "white" className="container">
      <Box
        height="100%"
        display="flex"
        flexDirection="column"
        gap="16px"
        bgcolor="black"
        justifyContent="center"
      >
        <Box
          height="100%"
          display="flex"
          flexDirection="row"
          gap="16px"
          justifyContent="center"
        >
          <Box
            height="100%"
            display="flex"
            flexDirection="column"
            gap="10px"
            bgcolor="black"
            justifyContent="center"
          >
            <h3 style={{color: 'black', backgroundColor: 'black'}} >sdf</h3>
            <h3 style={{color: 'white', backgroundColor: 'black'}} >{time}</h3>
            <Box sx={{
              display: "flex",
              justifyContent: "space-around",
              gap: "8px",
              height: "7vh",
            }}>
              <MPHandTurnSignal mph={54} leftTurn={true} rightTurn={true}/>
            </Box>
            <GearState state={"Reverse"}/>
            <OnePedalDrive value={ data.throttle.length !== 0 ? data.throttle[data.throttle.length - 1].value : 50 } />
            <AlertBox data={stringArrayData.BPSError.concat(stringArrayData.MotorControllerError, stringArrayData.PowerAuxError)}/>
          </Box>
          <Box
            height="100%"
            display="flex"
            flexDirection="column"
            gap="16px"
            justifyContent="center"
          >
            <VideoFeed />

          </Box>
        </Box>
        <Box
          height="100%"
          display="flex"
          flexDirection="row"
          gap="10px"
          justifyContent="center"
          width = "60%"
          marginLeft="19%"
        >
          <BatteryDischarge bat_discharge={67} darkMode={true} />
          <RPM rpm={data.motor_rpm.length !== 0 ? data.motor_rpm[data.motor_rpm.length - 1].value : 0} darkMode={true}/>
          <BatteryTempGuage temp={300} darkMode={true}/>
        </Box>
      </Box>
    </Box>
  );
};

export default HeadsUpPage;