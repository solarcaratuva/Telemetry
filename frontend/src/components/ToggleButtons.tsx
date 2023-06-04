import * as React from "react";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import { Box } from "@mui/material";
import Typography from "@mui/material/Typography";

interface Props {
  leftOn: boolean;
  rightOn: boolean;
  left: string;
  right: string;
  label: string;
}

const ToggleButtons: React.FC<Props> = ({ leftOn, rightOn, left, right, label }) => {
  return (
    <Box>
      <Typography> {label} </Typography>
      <ToggleButtonGroup
        value={leftOn ? "left" : (rightOn ? "right" : "None")}
        exclusive
        disabled
        aria-label="text alignment"
      >
        <ToggleButton value="left" aria-label="left aligned">
          {left}
        </ToggleButton>
        <ToggleButton value="right" aria-label="centered">
          {right}
        </ToggleButton>
      </ToggleButtonGroup>
    </Box>
  );
};

export default ToggleButtons;
