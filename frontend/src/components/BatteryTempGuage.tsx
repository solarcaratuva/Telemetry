import {Box, Paper, Typography } from "@mui/material";

import React from "react";
import ReactSpeedometer from "react-d3-speedometer";

interface Props {
  temp: number;
}

const BatteryTempGuage: React.FC<Props> = ({ temp}) => {


  return (
    <Box flex="1 0 0">
      <Paper sx={{ p: 2 }} elevation={2}>
        <Typography variant="h5" pb={1}>
          Battery Temp
        </Typography>
        <Box>
          {
            <ReactSpeedometer value={temp} />
          }
        </Box>
      </Paper>
    </Box>
  );
};

export default BatteryTempGuage;