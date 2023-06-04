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
import CurrentGuage from "../components/BatteryDischargeGuage";
import { Data, Update, StringData, StringUpdate, StringArrayData, StringArrayUpdate, BooleanData, BooleanUpdate } from './UpdateTypes';

const socket = io("http://localhost:5050");
const MAX_LENGTH = 50;

// TODO - refactor into class then have hud and monitors subclass, reuse data functionality
const HeadsUpPage = () => {
  const [data, setData] = useState<Data>({
    car_speed: [],
    battery_temp: [],
    panel_temp: [],
    throttle: [],
    hazards: [],
    brake_lights: [],
    forward_en: [],
    motor_rpm: [],
    total_current: [],
    high_temperature: []
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

  useEffect(()=>{
    const intervalId = setInterval(()=>{
      // const brakeLightsEnabled = data.brake_lights.length == 0 || data.brake_lights[data.brake_lights.length - 1];
      // const flashHazards = data.hazards.length == 0 || data.hazards[data.hazards.length - 1];
      // console.log("left: " + data.left_turn_signal.join(", "));
      // console.log("right: " + data.right_turn_signal.join(", "));
      // data.left_turn_signal.forEach((val) => {
      //   console.log("left: " + val.value);
      // })
      // console.log("left: " + booleanData.left_turn_signal);
      // console.log("right: " + booleanData.right_turn_signal);
      if (booleanData.left_turn_signal) {
        // console.log("flash left");
        setLeftBlinker((oldValue) => {
          return !oldValue;
        });
        setRightBlinker((oldValue) => {
          return false;
        });
      } else if (booleanData.right_turn_signal) {
        setRightBlinker((oldValue) => {
          return !oldValue;
        });
        setLeftBlinker((oldValue) => {
          return false;
        });
      } else {
        setLeftBlinker((oldValue) => {
          return false;
        });
        setRightBlinker((oldValue) => {
          return false;
        });
      }
    }, 500);
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
    <Box  height="100vh" boxSizing="border-box" bgcolor = "white" className="container">
      <Box
        height="100%"
        display="flex"
        flexDirection="column"
        gap="16px"
        bgcolor="white"
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
            bgcolor="white"
            justifyContent="center"
          >
            <h3 style={{color: 'white', backgroundColor: 'black'}} ></h3>
            <h3 style={{color: 'black', backgroundColor: 'white'}} >{time}</h3>
            <Box sx={{
              display: "flex",
              justifyContent: "space-around",
              gap: "8px",
              height: "7vh",
            }}>
              {/*tire diameter = 20.472in
                C = pi*diameter
                M/H = M/60min = 60 in/ 63360min = 60*20.472*pi/63360 * rpm
              */}
              <MPHandTurnSignal mph={data.motor_rpm.length !== 0 ? Math.floor(data.motor_rpm[data.motor_rpm.length - 1].value * 60*20.472*Math.PI/63360) : 0} leftTurn={leftBlinker} rightTurn={rightBlinker}/>
            </Box>
            <GearState state={booleanData.forward_en ? "Forward" : (booleanData.reverse_en ? "Reverse" : "Park")}/>
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
            <Box
              height="100%"
              display="flex"
              flexDirection="row"
              gap="10px"
              justifyContent="center"
              width = "60%"
              marginLeft="19%"
            >
              <CurrentGuage current={data.total_current.length !== 0 ? data.total_current[data.total_current.length - 1].value : 0} darkMode={false} />
              <BatteryTempGuage temp={data.high_temperature.length !== 0 ? data.high_temperature[data.high_temperature.length - 1].value : 0} darkMode={false}/>
            </Box>
          </Box>
        </Box>

      </Box>
    </Box>
  );
};

export default HeadsUpPage;