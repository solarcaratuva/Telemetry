import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState } from "react";

import OnePedalDrive from "../components/OnePedalDrive";
import { io } from "socket.io-client";
import ToggleButtons from "../components/ToggleButtons";
import AlertBox from "../components/AlertBox";
import RPM from "../components/RPM";

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

type StringDataSet = { value: string; timestamp: Date }[];
interface StringData {
  gear_state: StringDataSet;
  hazard_state: StringDataSet;
  turn_state: StringDataSet;
}
interface StringUpdate {
  string: string;
  timestamp: string;
}

const InteractivePage = () => {
  const [data, setData] = useState<Data>({
    car_speed: [],
    battery_temp: [],
    panel_temp: [],
    pedal_value: [],
  });

  const [stringData, setStringData] = useState<StringData>({
    gear_state: [],
    hazard_state: [],
    turn_state: [],
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

    Object.keys(stringData).forEach((name) => {
      socket.on(name, (update: StringUpdate) => {
        console.log(update)
        setStringData((oldData) => {
          const updatedData = {
            ...oldData,
            [name]: [
              ...oldData[name as keyof StringData],
              { value: update.string, timestamp: new Date(update.timestamp) },
            ],
          };
          if (updatedData[name as keyof StringData].length > MAX_LENGTH) {
            updatedData[name as keyof StringData] = updatedData[name as keyof StringData].slice(-MAX_LENGTH);
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
              <RPM  rpm={50}/>
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
              <ToggleButtons
                state={ stringData.gear_state.length != 0 ? stringData.gear_state[stringData.gear_state.length - 1].value : "false" }
                left={"Low"}
                right={"High"}
                label={"Gear:"}
              />
              <ToggleButtons
                state={ stringData.hazard_state.length != 0 ? stringData.hazard_state[stringData.hazard_state.length - 1].value : "false" }
                left={"Off"}
                right={"On"}
                label={"Hazard State:"}
              />
              <ToggleButtons
                state={ stringData.turn_state.length != 0 ? stringData.turn_state[stringData.turn_state.length - 1].value : "false" }
                left={"Left"}
                right={"Right"}
                label={"Turn Signal:"}
              />
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
                    <AlertBox data={["Alert 1", "Alert2"]}/>
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
