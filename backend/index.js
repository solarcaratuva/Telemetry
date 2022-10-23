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

let running = false;
for (let i = 0; i < 10 && !running; i++) {
  try {
    server.listen(5000, () => {
      running = true;
      console.info(`WSS listening on http://localhost:${5000 + i}`);
    });
  } catch (e) {
    console.info(`Port ${5000 + i} is already in use. Trying next port...`);
  }
}

/**
 * This is an example of sending data over the websocket.
 * Feel free to add more intervals and labels other than "message" to use for different features
 */

setInterval(() => {
  //Random integer between 0 and 100
  const number = Math.floor(Math.random() * 100);
  const timestamp = new Date().toISOString();
  io.to("connections").emit("message", {
    timestamp,
    number,
  });
}, 1000);
