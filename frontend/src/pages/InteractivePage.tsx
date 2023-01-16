import { Box, Button, Paper, Typography } from "@mui/material";
import { useEffect, useState } from "react";

import OnePedalDrive from "../components/OnePedalDrive";
import { io } from "socket.io-client";

const socket = io("http://localhost:5050");
const MAX_LENGTH = 50;

type DataSet = { value: number; timestamp: Date }[];
interface Data {
  car_speed: DataSet;
  battery_temp: DataSet;
  panel_temp: DataSet;
  pedal_value: DataSet;
}

interface Update {
  number: number;
  timestamp: string;
}

const InteractivePage = () => {
  const [data, setData] = useState<Data>({
    car_speed: [],
    battery_temp: [],
    panel_temp: [],
    pedal_value: [],
  });

  useEffect(() => {
    //Attaches socket listeners for each value of the data object on mount
    Object.keys(data).forEach((name) => {
      socket.on(name, (update: Update) => {
        setData((oldData) => {
          const updatedData = {
            ...oldData,
            [name]: [
              ...oldData[name as keyof Data],
              { value: update.number, timestamp: new Date(update.timestamp) },
            ],
          };
          if (updatedData[name as keyof Data].length > MAX_LENGTH) {
            updatedData[name as keyof Data] = updatedData[name as keyof Data].slice(-MAX_LENGTH);
          }
          return updatedData;
        });
      });
    });

    //Removes all socket listeners for each value of the data object on unmount
    //This is to prevent multiple listeners from being attached to the same value
    return () => {
      Object.keys(data).forEach((name) => {
        socket.off(name);
      });
    };
  }, []);

  return (
    <Box p="16px" height="100vh" boxSizing="border-box">
      {/* Page is vertically centered and will adapt based on actual component sizes */}
      <Box
        height="100%"
        display="flex"
        flexDirection="column"
        gap="16px"
        justifyContent="center"
      >
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-around",
            gap: "16px",
            height: "33vh",
          }}
        >
          {/* Replace this paper component with motor temp */}
          <Paper
            sx={{
              flex: "1 0 0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Typography>Motor Temp</Typography>
          </Paper>
          {/* Replace this paper component with RPM */}
          <Paper
            sx={{
              flex: "1 0 0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Typography>RPM</Typography>
          </Paper>
          {/* Replace this paper component with battery pack temp */}
          <Paper
            sx={{
              flex: "1 0 0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Typography>Battery Pack Temp</Typography>
          </Paper>
          {/* Replace this paper component with discharge */}
          <Paper
            sx={{
              flex: "1 0 0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Typography>Discharge</Typography>
          </Paper>
        </Box>
        <Box sx={{ display: "flex", gap: "16px", width: "100%" }}>
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-around",
              gap: "16px",
              width: "100%",
            }}
          >
            <Box
              sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-around",
                gap: "16px",
                height: "40vh",
                flex: "1 0 0",
              }}
            >
              {/* Replace this paper component with gear state */}
              <Paper
                sx={{
                  flex: "1 0 0",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Typography>Gear State</Typography>
              </Paper>
              {/* Replace this paper component with hazard state */}
              <Paper
                sx={{
                  flex: "1 0 0",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Typography>Hazard State</Typography>
              </Paper>
              {/* Replace this paper component with blinker state */}
              <Paper
                sx={{
                  flex: "1 0 0",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Typography>Blinker State</Typography>
              </Paper>
            </Box>
            <Box
              sx={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-around",
                gap: "16px",
                flex: "3 0 0",
              }}
            >
              <OnePedalDrive value={ data.pedal_value.length != 0 ? data.pedal_value[data.pedal_value.length - 1].value : 50 } />
              <Box
                sx={{
                  display: "flex",
                  justifyContent: "space-around",
                  gap: "16px",
                }}
              >
                {/* Replace this paper component with motor faults */}
                <Paper
                  sx={{
                    flex: "1 0 0",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    height: "calc(25vh - 8px)",
                  }}
                >
                  <Typography>Motor Faults</Typography>
                </Paper>
                {/* Replace this paper component with fifa chart */}
                <Paper
                  sx={{
                    flex: "1 0 0",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    height: "calc(25vh - 8px)",
                  }}
                >
                  <Typography>Fifa Chart</Typography>
                </Paper>
              </Box>
            </Box>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default InteractivePage;
