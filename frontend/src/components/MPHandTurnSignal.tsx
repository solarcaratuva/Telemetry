import React from "react";
// @ts-ignore
import Arrow from "react-arrow";
import {Box} from "@mui/material";

interface Props {
}

const MPHandTurnSignal: React.FC<Props> = () => {


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
        <Arrow
          direction="left" //sus af
          shaftWidth={20}
          shaftLength={24}
          headWidth={60}
          headLength={30}
          fill="black"
          stroke="green"
          strokeWidth={4}
        />
        <Box>
          <h1 style={{ fontSize: '50px', color: "white"}}>37</h1>
          {/*<Box height="70%">*/}
          {/*  <h3>37</h3>*/}
          {/*</Box>*/}
          {/*<Box height="30%"><h1>.</h1></Box>*/}
        </Box>
        <Arrow
          direction="right"
          shaftWidth={20} 
          shaftLength={24}
          headWidth={60}
          headLength={30}
          fill="black"
          stroke="green"
          strokeWidth={4}
        />
      </Box>
    </Box>
  );
};

export default MPHandTurnSignal;