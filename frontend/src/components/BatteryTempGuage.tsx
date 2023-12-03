import {Box, Typography } from "@mui/material";

import React from "react";
import ReactSpeedometer from "react-d3-speedometer";

interface Props {
  temp: number;
  darkMode: boolean;
}

const BatteryTempGuage: React.FC<Props> = ({ temp, darkMode}) => {


  return (
    <Box flex="1 0 0">
        <Typography variant="h5" color = {darkMode ? "white" : "black"} pb={1}>
          Battery Temperature
        </Typography>
        <Box>
          {
            <ReactSpeedometer textColor = {darkMode ? "white" : "black"} minValue={0} maxValue={300} segments={3} segmentColors={["#2ffc31", "#f0ff55","#fc312f"]}value={temp} />
          }
        </Box>
    </Box>
  );
};

export default BatteryTempGuage;