import { AxisOptions, Chart, ChartOptions } from "react-charts";
import { Box, Paper, Typography } from "@mui/material";

import React from "react";

interface DataPoint {
  timestamp: Date;
  value: number;
}

interface Props {
  data: { [label: string]: DataPoint[] };
  title: string;
}

/*
 * TODO:
 * Add a legend
 * Add a focus event to emphasise one line
 * Fix the tooltip location somehow
 */
const LineChart: React.FC<Props> = ({ data, title }) => {
  const primaryAxis = React.useMemo(
    (): AxisOptions<DataPoint> => ({
      getValue: (datum) => datum.timestamp,
    }),
    []
  );

  const secondaryAxes = React.useMemo(
    (): AxisOptions<DataPoint>[] => [
      {
        getValue: (datum) => datum.value,
        min: 0,
      },
    ],
    []
  );

  const newData = Object.entries(data).map(([label, data]) => ({
    label,
    //Show a default value of zero to prevent errors in the chart component
    data: data.length ? data : [{ timestamp: new Date(), value: 0 }],
  }));

  const options: ChartOptions<DataPoint> = {
    data: newData,
    primaryAxis,
    secondaryAxes,
  };

  return (
    <Box flex="1 0 0">
      <Paper sx={{ p: 2 }} elevation={2}>
        <Typography variant="h5" pb={1}>
          {title}
        </Typography>
        <Box height="300px" position="relative">
          <Chart options={options} />
        </Box>
      </Paper>
    </Box>
  );
};

export default LineChart;
