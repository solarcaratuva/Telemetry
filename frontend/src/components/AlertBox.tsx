import { AxisOptions, Chart, ChartOptions } from "react-charts";
import {Alert, Box, Paper, Typography } from "@mui/material";

import React from "react";

interface Props {
  data: string[];
}

/*
 * TODO:
 * Add a legend
 * Add a focus event to emphasise one line
 * Fix the tooltip location somehow
 */
const AlertBox: React.FC<Props> = ({ data}) => {


  return (
    <Box flex="1 0 0">
      <Paper sx={{ p: 2 }} elevation={2}>
        <Typography variant="h5" pb={1}>
          Motor Fault Alerts
        </Typography>
        <Box>
            {
                data.map((alert) => {
                        return (<Alert severity="warning">{alert}</Alert>);
                })
            }
        </Box>
      </Paper>
    </Box>
  );
};

export default AlertBox;