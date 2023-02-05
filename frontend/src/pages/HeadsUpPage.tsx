import {Box, Paper, Typography} from "@mui/material";
import React, {useEffect, useState} from "react";
import VideoFeed from "../components/VideoFeed";
import OnePedalDrive from "../components/OnePedalDrive";
import {io} from "socket.io-client";
import ReactSpeedometer from "react-d3-speedometer";
import AlertBox from "../components/AlertBox";
import RPM from "../components/RPM";
import BatteryTempGuage from "../components/BatteryTempGuage";

const socket = io("http://localhost:5050");
const MAX_LENGTH = 50;

type DataSet = { value: number; timestamp: Date }[];
interface Data {
  car_speed: DataSet;
  battery_temp: DataSet;
  panel_temp: DataSet;
  pedal_value: DataSet;
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
}
interface StringUpdate {
  string: string;
  timestamp: string;
}


const HeadsUpPage = () => {
  const [data, setData] = useState<Data>({
    car_speed: [],
    battery_temp: [],
    panel_temp: [],
    pedal_value: [],
  });

  const [stringData, setStringData] = useState<StringData>({
    gear_state: [],
    hazard_state: [],
    turn_state: [],
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

    //Removes all socket listeners for each value of the data object on unmount
    //This is to prevent multiple listeners from being attached to the same value
    return () => {
      Object.keys(data).forEach((name) => {
        socket.off(name);
      });
    };
  }, []);

  return (
    <Box p="16px" height="100vh" boxSizing="border-box" className="container">
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
          gap="16px"
          justifyContent="center"
        >
          <h3>{time}</h3>
          <Box sx={{
            display: "flex",
            justifyContent: "space-around",
            gap: "16px",
            height: "33vh",
          }}>
            {/* Replace this paper component with mph */}
            <Paper
              sx={{
                flex: "1 0 0",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Typography>MPH</Typography>
            </Paper>
          </Box>
          <OnePedalDrive value={ data.pedal_value.length !== 0 ? data.pedal_value[data.pedal_value.length - 1].value : 50 } />
          <AlertBox data={ data.battery_temp.length !== 0 && data.battery_temp[0].value>50 ? ["high bat tmp"] : ["test alert"] }/>
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
            gap="16px"
            justifyContent="center"
          >
            <RPM  rpm={500}/>
            <BatteryTempGuage temp={300}/>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default HeadsUpPage;