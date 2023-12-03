import React, {useEffect, useState} from "react";
// @ts-ignore
import Arrow from "react-arrow";
import {Box} from "@mui/material";

interface Props {
  mph: number,
  leftTurn: boolean,
  rightTurn: boolean
}

const MPHandTurnSignal: React.FC<Props> = ({mph, leftTurn, rightTurn}) => {

  // const [leftSignal, setLeftSignal] = useState(false);
  //
  // useEffect(()=>{
  //   const intervalId = setInterval(()=>{
  //     setLeftSignal(leftSignal => leftTurn ? !leftSignal : false);
  //   }, 500);
  //   return ()=>{clearInterval(intervalId)};
  // }, []);
  //
  // const [rightSignal, setRightSignal] = useState(false);
  //
  // useEffect(()=>{
  //   const intervalId = setInterval(()=>{
  //     setRightSignal(rightSignal => rightTurn ? !rightSignal : false);
  //   }, 500);
  //   return ()=>{clearInterval(intervalId)};
  // }, []);

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
          fill={leftTurn ? "green" : "white"}
          stroke="green"
          strokeWidth={4}
        />
        <Box>
          <h1 style={{ fontSize: '50px', color: "black"}}>{mph}</h1>
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
          fill={rightTurn ? "green" : "white"}
          stroke="green"
          strokeWidth={4}
        />
      </Box>
    </Box>
  );
};

export default MPHandTurnSignal;