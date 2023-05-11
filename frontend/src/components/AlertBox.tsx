import {Alert, Box, Paper, Typography } from "@mui/material";

import React from "react";

interface Props {
  data: string[];
}

const AlertBox: React.FC<Props> = ({ data}) => {


  return (
    <Box flex="1 0 0">
      <Paper sx={{ p: 2 }} elevation={2}>
        <Typography variant="h5" pb={1}>
          Errors
        </Typography>
        <Box>
            {
                data.map((alert) => {
                        return (<Alert severity="warning">{alert}</Alert>);
                })
            }
        </Box>
      </Paper>
    </Box>
  );
};

export default AlertBox;