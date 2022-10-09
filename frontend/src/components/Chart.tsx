import React from "react";
import { Box } from "@mui/material";

interface DataPoint {
  timestamp: Date;
  value: number;
}

interface Props {
  data: { [label: string]: DataPoint[] };
}

const Chart: React.FC<Props> = ({ data }) => {
  return <Box></Box>;
};

export default Chart;
