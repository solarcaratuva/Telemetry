import React, { useState } from "react";

import { Box } from "@mui/material";
import LineChart from "../components/LineChart";
import { io } from "socket.io-client";

const socket = io("http://localhost:5050");

const InteractivePage = () => {
  //This is just an example for how to use the websocket
  const [value, setValue] = useState(0);
  socket.on("message", (data: { number: number }) => {
    setValue(data.number);
  });

  const data = {
    "Sensor 1": [
      { timestamp: new Date(), value: 4 },
      {
        timestamp: new Date(new Date().getTime() + 10000),
        value: Math.random() * 10,
      },
      {
        timestamp: new Date(new Date().getTime() + 20000),
        value: Math.random() * 10,
      },
      {
        timestamp: new Date(new Date().getTime() + 30000),
        value: Math.random() * 10,
      },
      {
        timestamp: new Date(new Date().getTime() + 40000),
        value: Math.random() * 10,
      },
      {
        timestamp: new Date(new Date().getTime() + 50000),
        value: Math.random() * 10,
      },
      {
        timestamp: new Date(new Date().getTime() + 60000),
        value: Math.random() * 10,
      },
    ],
    "Sensor 2": [
      { timestamp: new Date(), value: 4 },
      {
        timestamp: new Date(new Date().getTime() + 10000),
        value: Math.random() * 10,
      },
      {
        timestamp: new Date(new Date().getTime() + 20000),
        value: Math.random() * 10,
      },
      {
        timestamp: new Date(new Date().getTime() + 30000),
        value: Math.random() * 10,
      },
      {
        timestamp: new Date(new Date().getTime() + 40000),
        value: Math.random() * 10,
      },
      {
        timestamp: new Date(new Date().getTime() + 50000),
        value: Math.random() * 10,
      },
      {
        timestamp: new Date(new Date().getTime() + 60000),
        value: Math.random() * 10,
      },
    ],
  };

  return (
    <Box>
      <h1>Interactive Page</h1>
      <p style={{ fontSize: "72px" }}>{value}</p>
      <LineChart data={data} />
    </Box>
  );
};

export default InteractivePage;
