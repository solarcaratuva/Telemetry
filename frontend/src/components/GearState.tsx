import React from "react";
// @ts-ignore
import Arrow from "react-arrow";
import {Box} from "@mui/material";


interface Props {
  state: string;
}

function getActive(dir: string) {
  return(
    <Box height="30px" bgcolor="white" paddingBottom="50px">
      <h1 style={{color: 'white', backgroundColor: 'black'}}>{dir}</h1>
    </Box>
  )
}

function getInActive(dir: string) {
  return(
    <Box height="30px" bgcolor="white" paddingBottom="50px">
      <h1 style={{color: 'black', backgroundColor: 'white'}}>{dir}</h1>
    </Box>
  )
}

const GearState: React.FC<Props> = ({state}) => {


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
        {state == "Forward" ? getActive("D") : getInActive("D")}
        {state == "Park" ? getActive("P") : getInActive("P")}
        {state == "Reverse" ? getActive("R") : getInActive("R")}
  </Box>
  </Box>
);
};

export default GearState;