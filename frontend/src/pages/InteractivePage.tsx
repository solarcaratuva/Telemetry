import { useEffect, useState } from "react";
import HoriBar from "../components/HoriBar";

import { Box, SpeedDial } from "@mui/material";
import LineChart from "../components/LineChart";
import { io } from "socket.io-client";
import { UpdateModeEnum } from "chart.js";

const socket = io("http://localhost:5050");

type DataSet = { value: number; timestamp: Date }[];
interface Data {
  speed: DataSet;
  battery_temp: DataSet;
  panel_temp: DataSet;
}

interface Update {
  number: number;
  timestamp: string;
}

const InteractivePage = () => {
  const [data, setData] = useState<Data>({
    speed: [],
    battery_temp: [],
    panel_temp: [],
  });

  useEffect(() => {
    //Attaches socket listeners for each value of the data object on mount
    Object.keys(data).forEach((name) => {
      socket.on(name, (update: Update) => {
        setData((oldData) => ({
          ...oldData,
          [name]: [
            ...oldData[name as keyof Data],
            { value: update.number, timestamp: new Date(update.timestamp) },
          ],
        }));
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
    <Box>
      <h1>Interactive Page</h1>
      <HoriBar value = {data.speed[data.speed.length-1].value} max = {100}/>
      <Box
        display="flex"
        gap="64px"
        width="100%"
        p="64px"
        boxSizing="border-box"
      >

        <Box flex="1 0 0">
          <LineChart data={{ Speed: data.speed }} title="Speed vs Time" />
         

        </Box> 
        <Box flex="1 0 0">
          <LineChart
            data={{
              "Battery Temp": data.battery_temp,
              "Solar Panel Temp": data.panel_temp,
            }}
            title="Temperatures vs Time"
          />
        </Box>
      </Box>
    </Box>
  );
};

export default InteractivePage;
