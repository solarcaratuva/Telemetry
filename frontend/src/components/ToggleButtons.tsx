import * as React from "react";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import { Box } from "@mui/material";
import Typography from "@mui/material/Typography";

interface Props {
  state?: string;
  left: string;
  right: string;
  label: string;
}

const ToggleButtons: React.FC<Props> = ({ state, left, right, label }) => {
  return (
    <Box>
      <Typography> {label} </Typography>
      <ToggleButtonGroup
        value={state}
        exclusive
        disabled
        aria-label="text alignment"
      >
        <ToggleButton value="false" aria-label="left aligned">
          {left}
        </ToggleButton>
        <ToggleButton value="true" aria-label="centered">
          {right}
        </ToggleButton>
      </ToggleButtonGroup>
    </Box>
  );
};

export default ToggleButtons;
