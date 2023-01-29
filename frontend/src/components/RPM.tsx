import {Box, Paper, Typography } from "@mui/material";

import React from "react";
import ReactSpeedometer from "react-d3-speedometer";

interface Props {
  rpm: number;
}

const RPM: React.FC<Props> = ({ rpm}) => {


  return (
    <Box flex="1 0 0">
      <Paper sx={{ p: 2 }} elevation={2}>
        <Typography variant="h5" pb={1}>
          RPM Guage
        </Typography>
        <Box>
            {
                <ReactSpeedometer value={rpm} />
            }
        </Box>
      </Paper>
    </Box>
  );
};

export default RPM;