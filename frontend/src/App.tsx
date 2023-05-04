import "./App.css";

import { BrowserRouter, Route, Routes } from "react-router-dom";

import InteractivePage from "./pages/InteractivePage";
import MonitorOnePage from "./pages/MonitorOnePage";
import MonitorTwoPage from "./pages/MonitorTwoPage";
import HeadsUpPage from "./pages/HeadsUpPage";
import { ThemeProvider } from "@emotion/react";
import { theme } from "./theme";
import React from "react";


function App() {
  return (
    <div className="App">
      <div
        style={{
          height: "100vh",
          width: "100vw",
          overflow: "hidden",
        }}
      >
        <ThemeProvider theme={theme}>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<HeadsUpPage />} />
              {/* <Route path="monitor_one" element={<MonitorOnePage />} /> //these appear to do nothing
              <Route path="monitor_two" element={<MonitorTwoPage />} /> */}
              <Route path="interactive_page" element={<InteractivePage />} />
            </Routes>
          </BrowserRouter>
        </ThemeProvider>
      </div>
    </div>
  );
}

export default App;
