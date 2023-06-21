import {Box, Typography } from "@mui/material";

import React from "react";
import ReactSpeedometer from "react-d3-speedometer";

interface Props {
  current: number;
  darkMode: boolean;
}

const CurrentGuage: React.FC<Props> = ({ current, darkMode}) => {


  return (
    <Box flex="1 0 0">
      <Typography variant="h5" color ={darkMode ? "white" : "black"} pb={1}>
        Net Current
      </Typography>
      <Box>
        {
          <ReactSpeedometer ringWidth={40} minValue={0} maxValue={100} segments={3} segmentColors={["#EDCBD2", "#80C4B7", "#E3856B"]} textColor = {darkMode ? "white" : "black"} value={current} />
        }
      </Box>
    </Box>
  );
};

export default CurrentGuage;