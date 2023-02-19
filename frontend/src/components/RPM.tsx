import {Box, Typography } from "@mui/material";

import React from "react";
import ReactSpeedometer from "react-d3-speedometer";

interface Props {
  rpm: number;
  darkMode: boolean;
}

const RPM: React.FC<Props> = ({ rpm, darkMode}) => {


  return (
    <Box flex="1 0 0">
        <Typography variant="h5" color ={darkMode ? "white" : "black"} pb={1}>
          RPM
        </Typography>
        <Box>
            {
                <ReactSpeedometer textColor = {darkMode ? "white" : "black"} value={rpm} />
            }
        </Box>
    </Box>
  );
};

export default RPM;