import React from "react";
// @ts-ignore
import Arrow from "react-arrow";
import {Box} from "@mui/material";

interface Props {
}

const GearState: React.FC<Props> = () => {


  return (
    <Box>
      <Box
        height="100%"
  display="flex"
  flexDirection="row"
  gap="16px"
  justifyContent="center"
  alignItems="center"
  >
        <Box bgcolor="black">
          <h1 style={{color: 'white', backgroundColor: 'black'}}>P</h1>
        </Box>
        <h1>R</h1>
        <h1>N</h1>
        <h1>D</h1>
  </Box>
  </Box>
);
};

export default GearState;