import {Box, Paper, Typography } from "@mui/material";

import React from "react";
import ReactSpeedometer from "react-d3-speedometer";

interface Props {
  rpm: number;
}

const RPM: React.FC<Props> = ({ rpm}) => {


  return (
    <Box flex="1 0 0">
        <Typography variant="h5" color = "white" pb={1}>
          RPM
        </Typography>
        <Box>
            {
                <ReactSpeedometer textColor = "white" value={rpm} />
            }
        </Box>
    </Box>
  );
};

export default RPM;