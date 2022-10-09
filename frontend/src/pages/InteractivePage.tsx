import { Box } from "@mui/material";
import React, { useState } from "react";
import { io } from "socket.io-client";

const socket = io("http://localhost:5000");

const InteractivePage = () => {
  //This is just an example for how to use the websocket
  const [value, setValue] = useState(0);
  socket.on("message", (data: { number: number }) => {
    setValue(data.number);
  });
  return (
    <Box>
      <h1>Interactive Page</h1>
      <p style={{ fontSize: "72px" }}>{value}</p>
    </Box>
  );
};

export default InteractivePage;
