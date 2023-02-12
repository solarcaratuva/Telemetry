import * as React from "react";
import Alert from "@mui/material/Alert";
import Stack from "@mui/material/Stack";

function overcurrent(over_current: number) {
  if (over_current == 1) {
    return (
      <Stack sx={{ width: "100%" }} spacing={2}>
        <Alert variant="filled" severity="error">
          Motor or Battery current is too high
        </Alert>
        <br />
      </Stack>
    );
  }
}
function hallsensor(hall_sensor: number) {
  if (hall_sensor == 1) {
    return (
      <Stack sx={{ width: "100%" }} spacing={2}>
        <Alert variant="filled" severity="error">
          Hall sensor is open/short circuit fault
        </Alert>
        <br />
      </Stack>
    );
  }
  return <></>;
}
function motorlocked(motor_locked: number) {
  if (motor_locked == 1) {
    return (
      <Stack sx={{ width: "100%" }} spacing={2}>
        <Alert variant="filled" severity="error">
          Motor Locked
        </Alert>
        <br />
      </Stack>
    );
  }
}
function sensorfault1(sensor_fault1: number) {
  if (sensor_fault1 == 1) {
    return (
      <Stack sx={{ width: "100%" }} spacing={2}>
        <Alert variant="filled" severity="error">
          Sensor Fault 1
        </Alert>
        <br />
      </Stack>
    );
  }
}
function sensorfault2(sensor_fault2: number) {
  if (sensor_fault2 == 1) {
    return (
      <Stack sx={{ width: "100%" }} spacing={2}>
        <Alert variant="filled" severity="error">
          Sensor Fault 2
        </Alert>
        <br />
      </Stack>
    );
  }
}
function highvoltage(high_voltage: number) {
  if (high_voltage == 1) {
    return (
      <Stack sx={{ width: "100%" }} spacing={2}>
        <Alert variant="filled" severity="error">
          High Battery Voltage
        </Alert>
        <br />
      </Stack>
    );
  }
}
function controlleroverheat(controller_overheat: number) {
  if (controller_overheat == 1) {
    return (
      <Stack sx={{ width: "100%" }} spacing={2}>
        <Alert variant="filled" severity="error">
          Controller Overheat
        </Alert>
        <br />
      </Stack>
    );
  }
}

interface Props {
  Over_current: number;
  Hall_sensor: number;
  Motor_locked: number;
  Sensor_fault1: number;
  Sensor_fault2: number;
  High_voltage: number;
  Controller_overheat: number;
}

const MotorFaults: React.FC<Props> = ({
  Over_current,
  Hall_sensor,
  Motor_locked,
  Sensor_fault1,
  Sensor_fault2,
  High_voltage,
  Controller_overheat,
}) => {
  return (
    <div>
      {overcurrent(Over_current)}
      {hallsensor(Hall_sensor)}
      {motorlocked(Motor_locked)}
      {sensorfault1(Sensor_fault1)}
      {sensorfault2(Sensor_fault2)}
      {highvoltage(High_voltage)}
      {controlleroverheat(Controller_overheat)}
    </div>
  );
};

export default MotorFaults;
