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
                    <ReactSpeedometer ringWidth={40} minValue={0} maxValue={40} customSegmentStops={[0, 15, 18, 22, 25, 40]} segmentColors={["#fc312f", "#f0ff55", "#2ffc31", "#f0ff55","#fc312f"]} textColor="black" value={voltage} />
                }
            </Box>
        </Box>
    );
};

export default CurrentGuage;