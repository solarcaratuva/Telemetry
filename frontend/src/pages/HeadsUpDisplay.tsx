import { Box } from "@mui/material";
import React from "react";
import VideoFeed from "../components/VideoFeed";

const HeadsUpDisplay = () => {
  return (
    <Box>
      <h1>Heads up</h1>
      <VideoFeed />
    </Box>
  );
};

export default HeadsUpDisplay;