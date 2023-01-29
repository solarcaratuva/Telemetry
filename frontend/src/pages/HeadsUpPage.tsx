import {Box, Paper, Typography} from "@mui/material";
import React, {useEffect, useState} from "react";
import VideoFeed from "../components/VideoFeed";
import OnePedalDrive from "../components/OnePedalDrive";
import {io} from "socket.io-client";
import ReactSpeedometer from "react-d3-speedometer";
import AlertBox from "../components/AlertBox";

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

  useEffect(() => {
    //Attaches socket listeners for each value of the data object on mount
    Object.keys(data).forEach((name) => {
      console.log("update name: " + name);
      socket.on(name, (update: Update) => {
        console.log("update name 2: " + name + update);
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
    <Box p="16px" height="100vh" boxSizing="border-box">
      <h1>Heads up</h1>
      <Box
        height="75%"
        display="flex"
        flexDirection="row"
        gap="16px"
        justifyContent="center"
      >
        <Box>
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
        <Box>
          <ReactSpeedometer />
          <Box>
          {/* Replace this paper component with mph */}
          <Paper
            sx={{
              flex: "1 0 0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <AlertBox data={["low bat", "sldkfj"]}/>
          </Paper>
        </Box>
          <VideoFeed />
        </Box>
      </Box>
      <OnePedalDrive value={ data.pedal_value.length !== 0 ? data.pedal_value[data.pedal_value.length - 1].value : 50 } />
    </Box>
  );
};

export default HeadsUpPage;