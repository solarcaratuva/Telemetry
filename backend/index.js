const express = require("express");
const app = express();
const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server, {
  cors: {
    origin: "http://localhost:3000",
    methods: ["GET", "POST"],
  },
});

io.on("connection", (socket) => {
  console.info("a user connected");
  socket.join("connections");
  socket.on("disconnect", (reason) => {
    console.info(`User has disconnected for reason: ${reason}`);
  });
});

server.listen(5050, () => {
  console.info("WSS listening on http://localhost:5050");
});

setInterval(() => {
  //Random integer between 0 and 100
  const number = Math.floor(Math.random() * 50 + 50);
  const timestamp = new Date().toISOString();
  io.to("connections").emit("car_speed", {
    timestamp,
    number,
  });
}, 2000);

setInterval(() => {
  //Random integer between 0 and 100
  const number = Math.floor(Math.random() * 100);
  const timestamp = new Date().toISOString();
  io.to("connections").emit("battery_temp", {
    timestamp,
    number,
  });
}, 2000);

setInterval(() => {
  //Random integer between 0 and 100
  const number = Math.floor(Math.random() * 100 + 50);
  const timestamp = new Date().toISOString();
  io.to("connections").emit("panel_temp", {
    timestamp,
    number,
  });
}, 2000);

setInterval(() => {
  //Random integer between 0 and 100
  const number = Math.floor(Math.random() * 256);
  const timestamp = new Date().toISOString();
  io.to("connections").emit("pedal_value", {
    timestamp,
    number,
  });
}, 2000);

setInterval(() => {
  //Random integer between 0 and 100
  const string = Math.random() > 0.5 ? "true" : "false";
  const timestamp = new Date().toISOString();
  io.to("connections").emit("gear_state", {
    timestamp,
    string,
  });
}, 2000);

setInterval(() => {
  //Random integer between 0 and 100
  const string = Math.random() > 0.5 ? "true" : "false";
  const timestamp = new Date().toISOString();
  io.to("connections").emit("hazard_state", {
    timestamp,
    string,
  });
}, 2000);

setInterval(() => {
  //Random integer between 0 and 100
  const string = Math.random() > 0.5 ? "true" : "false";
  const timestamp = new Date().toISOString();
  io.to("connections").emit("turn_state", {
    timestamp,
    string,
  });
}, 2000);