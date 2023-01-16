import { Box, Slider, Typography, lighten } from "@mui/material";
import React, { useState } from "react";

import { theme } from "../theme";

interface Props {
  value: number;
}

const OnePedalDrive: React.FC<Props> = ({ value }) => {
  const height = 25;
  //Which direction the bar will be in
  const isAccelerating = value > 75;
  //Whether the blue bar will be rendered
  const blue = isAccelerating ? value > 100 : value < 50;
  //Percentage (0 - 1) of max width of grey bar
  const greyWidth = blue
    ? 1
    : isAccelerating
    ? (value - 75) / 25
    : (75 - value) / 25;
  //Percentage (0 - 1) of max width of blue bar
  const blueWidth = !blue
    ? 0
    : isAccelerating
    ? (value - 100) / 155
    : (50 - value) / 50;

  return (
    <Box>
      <Box
        width="100%"
        display="flex"
        borderRadius={`${height / 2}px`}
        overflow="hidden"
        sx={{ bgcolor: theme.palette.disabled.main }}
      >
        <Box flex="75 0 0" display="flex">
          {!isAccelerating && (
            <>
              <Box flex="50 0 0" display="flex" justifyContent="flex-end">
                <Box
                  sx={{
                    bgcolor: theme.palette.primary.main,
                    width: `${blueWidth * 100}%`,
                    height: `${height}px`,
                  }}
                />
              </Box>
              <Box flex="25 0 0" display="flex" justifyContent="flex-end">
                <Box
                  sx={{
                    bgcolor: lighten(theme.palette.primary.main, 0.25),
                    width: `${greyWidth * 100}%`,
                    height: `${height}px`,
                  }}
                />
              </Box>
            </>
          )}
        </Box>
        <Box height={`${height}px`} width="2px" bgcolor="black" />
        <Box flex="180 0 0" display="flex">
          {isAccelerating && (
            <>
              <Box flex="25 0 0">
                <Box
                  sx={{
                    bgcolor: lighten(theme.palette.primary.main, 0.25),
                    width: `${greyWidth * 100}%`,
                    height: `${height}px`,
                  }}
                />
              </Box>
              <Box flex="155 0 0">
                <Box
                  sx={{
                    bgcolor: theme.palette.primary.main,
                    width: `${blueWidth * 100}%`,
                    height: `${height}px`,
                  }}
                />
              </Box>
            </>
          )}
        </Box>
      </Box>
      <Box width="100%" display="flex" justifyContent="space-between" py="8px">
        <Typography>Decelerating</Typography>
        <Typography>Accelerating</Typography>
      </Box>
    </Box>
  );
};

export default OnePedalDrive;
