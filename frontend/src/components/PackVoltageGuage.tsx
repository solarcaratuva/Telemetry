import {Box, Typography } from "@mui/material";

import React from "react";
import ReactSpeedometer from "react-d3-speedometer";

interface Props {
    voltage: number;
}

const CurrentGuage: React.FC<Props> = ({ voltage }) => {


    return (
        <Box flex="1 0 0">
            <Typography variant="h5" color="black" pb={1}>
                Pack Voltage
            </Typography>
            <Box>
                {
                    <ReactSpeedometer ringWidth={40} minValue={0} maxValue={100} segments={3} segmentColors={["#EDCBD2", "#80C4B7", "#E3856B"]} textColor="black" value={voltage} />
                }
            </Box>
        </Box>
    );
};

export default CurrentGuage;