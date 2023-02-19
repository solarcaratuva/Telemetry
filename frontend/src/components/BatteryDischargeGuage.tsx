import {Box, Typography } from "@mui/material";

import React from "react";
import ReactSpeedometer from "react-d3-speedometer";

interface Props {
  bat_discharge: number;
  darkMode: boolean;
}

const BatteryDischarge: React.FC<Props> = ({ bat_discharge, darkMode}) => {


  return (
    <Box flex="1 0 0">
      <Typography variant="h5" color ={darkMode ? "white" : "black"} pb={1}>
        Discharge
      </Typography>
      <Box>
        {
          <ReactSpeedometer textColor = {darkMode ? "white" : "black"} value={bat_discharge} />
        }
      </Box>
    </Box>
  );
};

export default BatteryDischarge;