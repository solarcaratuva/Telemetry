import React from "react";

import Alert, {AlertColor} from "@mui/material/Alert";

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
} from "recharts";

//Generate Fake Data (data is scaled from 0-10)
var Apoke = Math.floor(Math.random() * 10);
var Bpoke = Math.floor(Math.random() * 10);
var Cpoke = Math.floor(Math.random() * 10);
var Dpoke = Math.floor(Math.random() * 10);
var Epoke = Math.floor(Math.random() * 10);

//fake operational data
/*
  var Apoke = 3;
  var Bpoke = 4;
  var Cpoke = 4;
  var Dpoke = 3;
  var Epoke = 3;
  */

//fake warning data
/*
  var Apoke = 3;
  var Bpoke = 7;
  var Cpoke = 7;
  var Dpoke = 3;
  var Epoke = 3;
  */

//fake error data
/*
  var Apoke = 3;
  var Bpoke = 9;
  var Cpoke = 9;
  var Dpoke = 3;
  var Epoke = 3;
  */

//Creates the variables for styling of the chart
var fill_color = "";
var stroke_color = "";
var fill_opacity = 0;

//Chart Labels
var MotorPack_Label = "Motor Pack Temp: " + Apoke;
var RPM_Label = "RPM: " + Bpoke;
var BatteryPackTemp_Label = "Battery Pack Temp: " + Cpoke;
var Discharge_Label = "Discharge: " + Dpoke;
var BatteryVoltage_Label = "Battery Voltage: " + Epoke;

const FifaChart = () => {
  // Sample data
  const data = [
    { name: MotorPack_Label, x: Apoke },
    { name: RPM_Label, x: Bpoke },
    { name: BatteryPackTemp_Label, x: Cpoke },
    { name: Discharge_Label, x: Dpoke },
    { name: BatteryVoltage_Label, x: Epoke },
  ];

  //arbitrary error threshold (out of 10)
  var danger_threshold = 8;
  //arbitrary warning threshold (out of 10)
  var max_green = 6;

  //MotorPack
  var MotorPackSeverity: AlertColor;
  var MotorPackErrorMessage = "";
  if (Apoke > max_green && Apoke < danger_threshold) {
    MotorPackSeverity = "warning";
    MotorPackErrorMessage = "Motor Pack Warning";
  } else if (Apoke >= danger_threshold) {
    MotorPackSeverity = "error";
    MotorPackErrorMessage = "Motor Pack Error";
  } else {
    MotorPackSeverity = "success";
    MotorPackErrorMessage = "Motor Pack Functional";
  }

  //RPM
  var RPMSeverity: AlertColor;
  var RPMErrorMessage = "";
  if (Bpoke > max_green && Bpoke < danger_threshold) {
    RPMSeverity = "warning";
    RPMErrorMessage = "RPM Warning";
  } else if (Bpoke >= danger_threshold) {
    RPMSeverity = "error";
    RPMErrorMessage = "RPM Error";
  } else {
    RPMSeverity = "success";
    RPMErrorMessage = "RPM Functional";
  }

  //Battery Pack
  var BatteryPackTempSeverity: AlertColor;
  var BatteryPackTempErrorMessage = "";
  if (Cpoke > max_green && Cpoke < danger_threshold) {
    BatteryPackTempSeverity = "warning";
    BatteryPackTempErrorMessage = "Battery Pack Temp Warning";
  } else if (Cpoke >= danger_threshold) {
    BatteryPackTempSeverity = "error";
    BatteryPackTempErrorMessage = "Battery Pack Temp Error";
  } else {
    BatteryPackTempSeverity = "success";
    BatteryPackTempErrorMessage = "Battery Pack Temp Functional";
  }

  //Discharge
  var DischargeSeverity: AlertColor;
  var DischargeErrorMessage = "";
  if (Dpoke > max_green && Dpoke < danger_threshold) {
    DischargeSeverity = "warning";
    DischargeErrorMessage = "Discharge Warning";
  } else if (Dpoke >= danger_threshold) {
    DischargeSeverity = "error";
    DischargeErrorMessage = "Discharge Error";
  } else {
    DischargeSeverity = "success";
    DischargeErrorMessage = "Discharge Functional";
  }

  var BatteryVoltageSeverity: AlertColor;
  var BatteryVoltageErrorMessage = "";
  if (Epoke > max_green && Epoke < danger_threshold) {
    BatteryVoltageSeverity = "warning";
    BatteryVoltageErrorMessage = "Battery Voltage Warning";
  } else if (Epoke >= danger_threshold) {
    BatteryVoltageSeverity = "error";
    BatteryVoltageErrorMessage = "Battery Voltage Error";
  } else {
    BatteryVoltageSeverity = "success";
    BatteryVoltageErrorMessage = "Battery Voltage Functional";
  }

  //If any error detected, set chart to red
  if (
    Apoke >= danger_threshold ||
    Bpoke >= danger_threshold ||
    Cpoke >= danger_threshold ||
    Dpoke >= danger_threshold ||
    Epoke >= danger_threshold
  ) {
    fill_color = "red";
    stroke_color = "black";
    fill_opacity = 0.8;
  }
  //If data is within warning range but below error, set to yellow
  else if (
    (Apoke > max_green && Apoke < danger_threshold) ||
    (Bpoke > max_green && Bpoke < danger_threshold) ||
    (Cpoke > max_green && Cpoke < danger_threshold) ||
    (Dpoke > max_green && Dpoke < danger_threshold) ||
    (Epoke > max_green && Epoke < danger_threshold)
  ) {
    fill_color = "yellow";
    stroke_color = "black";
    fill_opacity = 0.75;
  }
  //else (everything is functional), set to green
  else {
    fill_color = "green";
    stroke_color = "black";
    fill_opacity = 0.5;
  }

  return (
    <React.Fragment>
      <div>
        <RadarChart height={500} width={500} outerRadius="50%" data={data}>
          <PolarGrid />
          <PolarAngleAxis dataKey="name" />
          <PolarRadiusAxis angle={45} domain={[0, 10]} tickCount={10} />
          <Radar
            dataKey="x"
            stroke={stroke_color}
            fill={fill_color}
            fillOpacity={fill_opacity}
          />
        </RadarChart>
      </div>
      <div>
        <Alert severity={MotorPackSeverity}>{MotorPackErrorMessage}</Alert>
        <Alert severity={RPMSeverity}>{RPMErrorMessage}</Alert>
        <Alert severity={BatteryPackTempSeverity}>
          {BatteryPackTempErrorMessage}
        </Alert>
        <Alert severity={DischargeSeverity}>{DischargeErrorMessage}</Alert>
        <Alert severity={BatteryVoltageSeverity}>
          {BatteryVoltageErrorMessage}
        </Alert>
      </div>
    </React.Fragment>
  );
};

export default FifaChart;

/*

Justification and Idea for Use Case: 
	The fifa chart to should summarize all the data on the display into one region of the screen.
	This way, rather than having to peer across all the gauges simultaneously at once, a viewer can passively focus on the fifa chart. When the fifa chart shows an error, the viewer will know exactly where to look. 
	The fifa chart should show all the data that is on the gauges, as well as potentially tracking the value of the motor faults to its left (for instance, showing battery voltage)
	Plus, this fifa chart is able to show trends in data by how the shape is is moving over time. Further, the viewer will be able to predict errors by noticing how the fifa chart grows towards an error in certain regions. 
	Although the data is likely redundant, it makes summarizing the data intuitive and easily understandable, as no numbers/computations are involved.


Current Ideas for Data Points (based off current dashboard drawing):
	-Motor Pack Temp
	- RPM
	- Battery Pack Temp
	- Discharge
	- Battery Voltage
	

How would the data be implemented?
	Rather than having the actual numerical values of each datapoint, the radar chart would show the percentage of safe value (experimentally determined) each given data point. 
	This way, all the data points are scaled to match one another, and there is no need to do any mental comparison beyond the visual representation.

How will the fifa chart show an error?
	The fifa chart will have 3 stages of operation. A Green, Yellow, and Red stage. 
	In the green stage, all data points are within their expected/regular/safe operating values. In this case, the radar chart will be filled with a soft green color. In this mode, the radar chart will generally mimic a regular polygon (such as a pentagon or octagon)	 			 
     	When one or more of the data points begins to approach its no-go operating levels, the chart should turn a darker, more solid shade of yellow. This will then tell the viewer that there is an error being approached at a certain data point (This is how we will predict errors). Now, the radar chart will be noticeably imbalanced and jagged on a certain edge; this asymmetric edge will be the error edge.
	When one or more of the data points reaches unsafe operation levels, the chart will fill with a solid, bold red. In this case, the radar chart will also change shape considerably and noticeably, having the error edge be sticking out aggressively from the center. 

*/
