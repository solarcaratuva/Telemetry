import { AxisOptions, Chart, ChartOptions } from "react-charts";
import { Box, Typography } from "@mui/material";

import React from "react";

interface DataPoint {
  timestamp: Date;
  value: number;
}

interface Props {
  data: { [label: string]: DataPoint[] };
}

const LineChart: React.FC<Props> = ({ data }) => {
  const primaryAxis = React.useMemo(
    (): AxisOptions<DataPoint> => ({
      getValue: (datum) => datum.timestamp.getTime(),
    }),
    []
  );

  const secondaryAxes = React.useMemo(
    (): AxisOptions<DataPoint>[] => [
      {
        getValue: (datum) => datum.value,
      },
    ],
    []
  );

  const newData = Object.entries(data).map(([label, data]) => ({
    label,
    data,
  }));

  const options: ChartOptions<DataPoint> = {
    data: newData,
    primaryAxis,
    secondaryAxes,
  };

  console.log(options);

  return (
    <Box>
      <Typography>Line chart</Typography>
      <Chart options={options} />
    </Box>
  );
};

export default LineChart;
